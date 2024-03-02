from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('create/<code>/<slug>/<name>', views.CreateArticle.as_view(), name="create"),
    path("delete/<slug>/<pk>", views.DeleteArticle.as_view(), name="delete"),
    path('article/<slug>/<int:pk>', views.DeleteArticle.as_view(), name="single"),

    path('all/<slug>', views.ArticleList.as_view(), name="all"),
    path('articles/<code>/<slug>/<name>', views.ArticlePage.as_view(), name='articles'),
    path('pending_articles/<code>/<slug>/<name>', views.PendingArticlePage.as_view(), name='pending_articles'),
    path('my_articles/<code>/<slug>/<name>', views.MyArticlePage.as_view(), name='my_articles'),

    path('update/<slug>/<int:pk>', views.UpdateArticle.as_view(), name="update"),
    path('updaterecord/<int:pk>', views.UpdateRecord, name="update_record"),

    path('view_article/<int:pk>', views.ViewArticle.as_view(), name="article_view"),
    path('add_comment/<int:pk>', views.AddComment, name="add_comment"),
]
