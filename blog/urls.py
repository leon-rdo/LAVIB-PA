from django.urls import path
from .views import IndexView, PostDetailView, CategoriesView

app_name = 'blog'

urlpatterns = [
    path("", IndexView.as_view(), name="blog_index"),
    path('<slug:slug>/', PostDetailView.as_view(), name="post_detail"),
    path("categorias/<category>/", CategoriesView.as_view(), name="categories"),
]
