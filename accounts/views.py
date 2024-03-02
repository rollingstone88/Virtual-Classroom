import os

from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView
from django.core.mail import EmailMessage

from . import forms
from .tokens import account_activation_token


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:confirm')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        dob = form.cleaned_data.get('birth_date')
        profile_pic = form.cleaned_data.get('profile_pic')
        print(profile_pic)
        print(dob)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user.profile.birth_date = dob
        user.profile.profile_pic = profile_pic

        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your Virtual Classroom Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()
        return super().form_valid(form)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class Confirm(TemplateView):
    template_name = 'accounts/confirmation.html'


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return redirect('accounts:login')
    else:
        form = forms.UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})


class ProfileView(TemplateView, LoginRequiredMixin, SelectRelatedMixin):
    template_name = 'accounts/profile_view.html'
    model = User

    def get_context_data(self, *args, **kwargs):
        myUser = User.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(*args, **kwargs)
        context['myUser'] = myUser

        return context


class ProfileSettings(TemplateView, LoginRequiredMixin, SelectRelatedMixin):
    template_name = 'accounts/profile_seetings.html'
    model = User

    def get_context_data(self, *args, **kwargs):
        myUser = User.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(*args, **kwargs)
        context['myUser'] = myUser

        return context


def UpdateProfile(request, *args, **kwargs):
    pk = kwargs.get('pk')

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    dob = request.POST['dob']
    user = User.objects.get(pk=pk)

    user.first_name = first_name
    user.last_name = last_name

    if dob:
        user.profile.birth_date = dob

    old_pass = request.POST['old_password'].strip()
    new_pass = request.POST['new_password'].strip()
    conf_new_pass = request.POST['conf_new_password'].strip()
    if old_pass and conf_new_pass and conf_new_pass == new_pass:
        if user.check_password(old_pass):
            user.set_password(request.POST['conf_new_password'])
        else:
            template = loader.get_template("password_change_error.html")
            return HttpResponse(template.render())
    elif old_pass or conf_new_pass or new_pass:
        template = loader.get_template("password_change_error.html")
        return HttpResponse(template.render())
    else:
        pass

    try:
        if request.FILES['profile_pic']:
            dir = "comment/"
            image = request.FILES['profile_pic']
            fss = FileSystemStorage()
            file = fss.save(dir + image.name, image)
            file_url = fss.url(file)
            user.profile.profile_pic = dir + os.path.basename(file_url)

        else:
            pass
    except:
        pass

    user.save()

    print(first_name)
    print(last_name)
    print(dob)

    return HttpResponseRedirect(
        reverse("accounts:profile_view", args=args, kwargs={"pk": pk}))
