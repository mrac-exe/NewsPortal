from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import render, get_object_or_404


class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.type = 'AR'
        post.author = self.request.user.author
        post.save()

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, template_name='post_lock.html', context=context)
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(DeleteView):
    permission_required = ('portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, template_name='post_lock.html', context=context)
        return super(PostDelete, self).dispatch(request, *args, **kwargs)


class CategoryList(ListView):
    model = Post
    template_name = 'categories_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_time')
        return queryset

    def get_context_data(self, **kwargs):
        context1 = super().get_context_data(**kwargs)
        context1['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context1['category'] = self.category
        return context1


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


