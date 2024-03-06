from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from .models import CustomUser, Post, Like
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy

def index(request):
    return render(request, "index.html")

class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'

# コードレビューの点未修正
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'mypost.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)

# コードレビューの点未修正
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
        context['following_users'] = self.request.user.following.all()
        return context

class LikeCreate(LoginRequiredMixin, CreateView):
    model = Like
    fields = []  # フォームに表示するフィールドはなし
    success_url = reverse_lazy('other_user_post_list')

    def form_valid(self, form):
        target = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.target = target  # Likeインスタンスのtargetフィールドに代入
        form.instance.user = self.request.user  # Likeインスタンスのuserフィールドに代入
        return super().form_valid(form)

# CreateViewではなく、Viewを継承した場合のコード

# class LikeCreate(LoginRequiredMixin, View):

#     def post(self, request, *args, **kwargs):
#         target = get_object_or_404(Post, pk=self.kwargs['pk'])
#         Like.objects.create(target=target, user=self.request.user)
#         return redirect('other_user_post_list')

class LikeDelete(LoginRequiredMixin, DeleteView):
    model = Like
    success_url = reverse_lazy('other_user_post_list')

    # デフォルトでは"どのオブジェクト"を削除するかしかDeleteViewは認識しないため、
    # "誰が""どのオブジェクト"を削除するかをオーバーライドして認識させる
    def get_object(self, queryset=None):
        target = get_object_or_404(Post, pk=self.kwargs['pk'])
        return get_object_or_404(Like, target=target, user=self.request.user)

# DeleteViewではなく、Viewを継承した場合のコード

# class LikeDelete(LoginRequiredMixin, View):

#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             like = Like.objects.filter(target_id=kwargs['pk'], user=request.user)
#         if like:
#             like.delete()
#         return redirect('other_user_post_list')

class Follow(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_to_follow = CustomUser.objects.get(pk=kwargs['pk'])
            request.user.following.add(user_to_follow)
            return HttpResponseRedirect(reverse('other_user_post_list'))
        
class Unfollow(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_to_unfollow = CustomUser.objects.get(pk=kwargs['pk'])
            request.user.following.remove(user_to_unfollow)
            return HttpResponseRedirect(reverse('other_user_post_list'))
