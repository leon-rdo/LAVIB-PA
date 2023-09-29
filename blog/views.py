from django.views import generic
from blog.models import Category, Post


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoriesView(generic.ListView):
    template_name = "blog/categories.html"
    context_object_name = "posts"

    def get_queryset(self):
        category = self.kwargs["category"]
        return Post.objects.filter(
            categories__category__contains=category
        ).order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        context["all_categories"] = Category.objects.all()
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["excluir_metatags"] = True
        return context