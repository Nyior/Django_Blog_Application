from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.

'''
def home(request): #this is a function based view
    context = {
       'posts' : Post.objects.all()
    }
    return render(request, 'my_blog_app/home.html', context)
'''

class PostListView(ListView):
    model = Post
    template_name = 'my_blog_app/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posed']
    paginate_by = 5 #I should have had fewer lines of code here. I had more
    #lines because i didnt stick to the naming convention. by default django looks for
    #a template <app>/model_viewtype and database objects with  name = object_list
class UserPostListView(ListView):
    model = Post
    template_name = 'my_blog_app/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posed')

def about(request):
    context = {
        'title': 'Application'
    }
    return render(request, "my_blog_app/about.html", context)


class PostDetailView(DetailView):
    model = Post

'''
this view sticks to all the convention. thus #thus we would have less code to write
here there is no template specified because by default django looks for and renders
 my_blog_app/post_detail which i created
and no context variable was explicitly passed to the template because django passes
the context variable with the name #object to the template
'''

class PostCreateView(LoginRequiredMixin, CreateView): #lrm secures a route to users
    #that are logged in
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #lrm secures a route to users
    #that are logged in
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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
