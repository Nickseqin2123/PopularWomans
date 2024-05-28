from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, get_object_or_404
from .forms import AddPostForm, UploadFileForm
from .models import Women, UploadFiles
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import DataMixin, menu


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    
    def get_queryset(self):
        return Women.published.all().select_related('cat')
    

def about(request: HttpRequest):
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    
    return render(request, 'women/about.html',
                  {'title': 'О сайте',
                   'menu': menu,
                   'form': form}
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


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ('title', 'content', 'photo', 'is_published', 'cat')
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактируемые статьи'
    

class PostDelete(DataMixin, DeleteView):
    model = Women
    success_url = reverse_lazy('home')
    template_name = 'women/delete_post.html'
    title_page = 'Удаление статьи'
    
    
def contact(request):
    return HttpResponse("Обратная связь")


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