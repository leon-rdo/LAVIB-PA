from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render
from blog.models import Category, Post, Commentary, Forbidden_Word
from .forms import CommentaryForm


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
        post = self.get_object()
        commentaries = Commentary.objects.filter(post=post)
        form = CommentaryForm()
        error_message = None
        forbidden_words = list(
            Forbidden_Word.objects.values_list("word", flat=True)
        )

        context["commentaries"] = commentaries
        context["form"] = form
        context["forbidden_words"] = forbidden_words
        context["error_message"] = error_message
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        commentaries = Commentary.objects.filter(post=post)
        form = CommentaryForm(request.POST)
        error_message = None
        forbidden_words = list(
            Forbidden_Word.objects.values_list("word", flat=True)
        )

        if form.is_valid():
            for word in forbidden_words:
                if word in form.cleaned_data["body"].lower():
                    error_message = "Seu comentário contém uma palavra proibida!"
                    break
            else:
                commentary = Commentary(
                    author=form.cleaned_data["author"],
                    body=form.cleaned_data["body"],
                    post=post,
                )
                commentary.save()
                commentaries = Commentary.objects.filter(post=post)
                # Redirect to the same page with a hash
                return redirect(f"{reverse('blog:post_detail', args=[post.slug])}#Commentary")


        context = self.get_context_data()
        context["commentaries"] = commentaries
        context["form"] = form
        context["forbidden_words"] = forbidden_words
        context["error_message"] = error_message
        return render(request, self.template_name, context)