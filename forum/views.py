from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView
from .models import Post, Comment, PostUpVotes, PostDownVotes
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


class Index(ListView):
    template_name = 'forum/index.html'

    def get_queryset(self):
        sort_method = '-date'

        try:
            if self.kwargs['sort_type'] == 'top':
                sort_method = '-total_votes'
            print(self.kwargs['sort_type'])
        except:
            pass

        return Post.objects.order_by(sort_method)


class Detail(DetailView):
    model = Post
    template_name = 'forum/detail.html'


class SubmitPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(SubmitPost, self).form_valid(form)

@login_required()
def comment(request, id):

    if request.method == 'POST':
        comm = CommentForm(request.POST)

        if comm.is_valid():
            commen = comm.save(commit=False)
            commen.post = Post.objects.get(pk=id)
            commen.user = request.user
            commen.save()
        else:
            print('Error')

    return HttpResponseRedirect(reverse('detail', args=(id,)))

class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('detail', args=(self.kwargs['post_id'],))

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('index')

class RegisterView(CreateView):
    model = User
    template_name = 'forum/login_view.html'
    success_url = reverse_lazy('index')
    form_class = UserCreationForm

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        usr = authenticate(username=self.request.POST['username'], password=self.request.POST['password1'])
        login(self.request, usr)
        return response

def up_vote_post(request, post_id, nxt):
    post = Post.objects.get(pk=post_id)
    try:
        PostUpVotes.objects.get(user=request.user, post=post).delete()
    except PostUpVotes.DoesNotExist:
        PostUpVotes.objects.create(user=request.user, post=post)
    try:
        PostDownVotes.objects.get(user=request.user, post=post).delete()
    except PostDownVotes.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse_lazy(nxt))

def down_vote_post(request, post_id, nxt):
    post = Post.objects.get(pk=post_id)
    try:
        PostDownVotes.objects.get(user=request.user, post=post).delete()
    except PostDownVotes.DoesNotExist:
        PostDownVotes.objects.create(user=request.user, post=post)
    try:
        PostUpVotes.objects.get(user=request.user, post=post).delete()
    except PostUpVotes.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse_lazy(nxt))
