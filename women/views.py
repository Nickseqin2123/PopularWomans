from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, get_object_or_404
from .forms import AddPostForm, ContactForm
from .models import Women
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.cache import cache
from .utils import DataMixin, menu
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    
    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 60)
        
        return w_lst


@login_required
def about(request: HttpRequest):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'women/about.html',
                  {'title': 'О сайте',
                   'menu': menu,
                   'current_obj': page_obj}
                  )


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)
    

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ('title', 'content', 'photo', 'is_published', 'cat')
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактируемые статьи'
    permission_required = 'women.change_women'
    

class PostDelete(DataMixin, DeleteView):
    model = Women
    success_url = reverse_lazy('home')
    template_name = 'women/delete_post.html'
    title_page = 'Удаление статьи'
    

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Обратная связь'
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title=f'Категория - {cat.name}',
                                      cat_selected=cat.id
                                    )


class WomenShowPosts(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag = context['posts'][0].tags.all()[0]
        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")