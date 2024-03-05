from django.db.models.query import QuerySet
from .models import Post, Like
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy

def index(request):
    return render(request, "index.html")

class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'allpost.html'

    def get_queryset(self):
        return Post.objects.all()
   
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'mypost.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)

class OtherUserPostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'other_user_post_list.html'

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes = Like.objects.filter(user=self.request.user)
        context['like_exists'] = {like.target.id: True for like in user_likes}
        context['user_likes'] = {like.target.id: like for like in user_likes}
        return context

class LikeCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        target = get_object_or_404(Post, pk=self.kwargs['pk'])
        Like.objects.create(target=target, user=self.request.user)
        return redirect('other_user_post_list')

class LikeDelete(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            like = Like.objects.filter(target_id=kwargs['pk'], user=request.user)
        if like:
            like.delete()
        return redirect('other_user_post_list')