from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

'''
posts = [
    {
        'author': 'Pritam',
        'title': 'Blog post 1',
        'content': 'First post content 1',
        'posted': 'September 16, 2020',
    },
    {
        'author': 'John Doe',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'posted': 'August 16, 2020',
    },

]
'''

def index(request):

    context = {
        'posts': Post.objects.all()
    }

    return render(request, "blog/index.html", context)


def about(request):
    return render(request, "blog/about.html", {'title': 'pritam'})


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
