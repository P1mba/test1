from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name =  'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Articles(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/main', null=True, blank=True)
    file = models.FileField(upload_to='files/main', null=True, verbose_name='Файлы')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name =  'Пост'
        verbose_name_plural = 'Посты'


    def __str__(self):
        return self.title