from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import Women


# Запуск тество python manage.py test <приложение> или . - все тесты или же конкретный тест <приложение>.tests.<класс тестов>.<имя метода>
class GetPageTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json'] # Фикстуры, которые будут загружаться перед каждым тестом
    # Для начала нужно сделать dumpdata
    
    def setUp(self) -> None: # Можно не прописывать
        '''Инициализация перед выполнением каждого теста'''
        return super().setUp()
    
    def test_page(self):
        '''test_ - тестируемый метод'''
        path = reverse('home')
        response = self.client.get(path) # GET - запрос к гланой странице
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')
        
    def test_register_redirect(self):
        path = reverse('add_page')
        redirectt = f'{reverse('users:login')}?next={path}'
        response = self.client.get(path) # GET - запрос к гланой странице
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirectt)        
    
    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])
        
    def test_paginate(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(f'{path}?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])
    
    def test_posts(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        resp = self.client.get(path)
        self.assertEqual(w.content, resp.context_data['post'].content)
    
    def tearDown(self) -> None: # Можно не прописывать
        '''Действие после выполнения каждого теста'''
        return super().tearDown()