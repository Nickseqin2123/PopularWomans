from typing import Any
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from django.views import View
from django.views.generic import ListView


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WomenHome(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.published.all().select_related('cat'),
        'cat_selected': 0,
    }
    
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


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


class AddPage(View):
    
    def get(self, request):
        form = AddPostForm()
        
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        
        return render(request, 'women/addpage.html', context=data)
    
    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        
        return render(request, 'women/addpage.html', context=data)
    

def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context
        
        
def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f"Тэг: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    
    return render(request, 'women/index.html', context=data)
    

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")