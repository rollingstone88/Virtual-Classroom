import os.path

from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView

from classroom.models import Classroom
from .forms import CommentForm
from .models import Article, ArticleComment


class CreateArticle(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = ("title", "description")

    def get_success_url(self):
        return reverse_lazy("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def form_valid(self, form):
        code = self.kwargs.get("code")
        classroom = Classroom.objects.get(code=code)
        article_count = Article.objects.filter(classroom__code=code, is_accepted=False).count()
        if article_count >= 10:
            html = "<html><body><h1>Number of Articles reached its limit for this classroom</h1></body></html>"
            return HttpResponse(html)

        self.object = form.save(commit=False)
        self.object.creator = self.request.user

        self.object.classroom = classroom
        self.object.save()
        return super().form_valid(form)


class ArticleList(SelectRelatedMixin, generic.ListView):
    model = Article
    select_related = ("creator", "classroom")

    def get_queryset(self):
        queryset = super().get_queryset()
        classroom = Classroom.objects.get(slug=self.kwargs.get('slug'))
        return queryset.filter(classroom=classroom)


class DeleteArticle(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Article
    select_related = ("creator", "classroom")

    def get_success_url(self):
        return reverse_lazy("classroom:single", kwargs={"slug": self.kwargs.get("slug")})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(creator_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Article Deleted")
        return super().delete(*args, **kwargs)


'''
class UpdateArticle(LoginRequiredMixin, generic.UpdateView):
    model = Article

'''


class ArticlePage(TemplateView):
    template_name = 'articles/article_showing_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()
        code = self.kwargs.get("code")
        context['classroom_code'] = code
        # print(self.request.POST.get('classroom_code'))
        return context


class PendingArticlePage(TemplateView):
    template_name = 'articles/pending_article_showing_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()
        code = self.kwargs.get("code")
        context['classroom_code'] = code

        return context


class MyArticlePage(TemplateView):
    template_name = 'articles/my_articles.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()
        code = self.kwargs.get("code")
        context['classroom_code'] = code
        context['user'] = self.request.user
        # print(self.request.POST.get('classroom_code'))
        return context


class UpdateArticle(TemplateView):
    template_name = 'articles/update_article.html'

    def get_context_data(self, *args, **kwargs):
        classroom = Classroom.objects.get(slug=self.kwargs.get('slug'))
        article = Article.objects.get(pk=self.kwargs.get('pk'), classroom=classroom)

        context = super().get_context_data(*args, **kwargs)

        context['article'] = article

        return context


def UpdateRecord(request, *args, **kwargs):
    pk = kwargs.get('pk')

    title = request.POST['title']
    description = request.POST['description']
    article = Article.objects.get(pk=pk)

    article.title = title
    article.description = description
    article.is_accepted = True
    article.save()

    classroom = article.classroom
    code = classroom.code
    slug = classroom.slug
    name = classroom.name
    return HttpResponseRedirect(
        reverse("article:articles", args=args, kwargs={"code": code, "slug": slug, "name": name}))


class ViewArticle(TemplateView, LoginRequiredMixin, SelectRelatedMixin):
    template_name = 'articles/article_view.html'
    model = Article
    fields = ("title", "description")

    def get_context_data(self, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))

        context = super().get_context_data(*args, **kwargs)
        context['article'] = article
        context['user'] = self.request.user

        comments = ArticleComment.objects.filter(article=article, classroom=article.classroom)
        # print(comments)
        context['comments'] = comments

        return context


def handle_uploaded_image(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def AddComment(request, *args, **kwargs):
    pk = kwargs.get('pk')

    comment_text = request.POST['comment']

    article = Article.objects.get(pk=pk)

    try:
        if request.FILES['image']:
            dir = "comment/"
            image = request.FILES['image']
            fss = FileSystemStorage()
            file = fss.save(dir + image.name, image)
            file_url = fss.url(file)
            comment = ArticleComment(classroom=article.classroom, student=request.user, comment_text=comment_text,
                                     comment_image=dir + os.path.basename(file_url),
                                     article=article)

        else:
            comment = ArticleComment(classroom=article.classroom, student=request.user, comment_text=comment_text,
                                     article=article)
    except:
        comment = ArticleComment(classroom=article.classroom, student=request.user, comment_text=comment_text,
                                 article=article)

    comment.save()
    return HttpResponseRedirect(
        reverse("article:article_view", args=args, kwargs={"pk": pk}))
