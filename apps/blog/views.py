from django.shortcuts import render
from django.urls import reverse

from apps.blog.models import BlogCategory, Article, Tag

def blog_category_list(request):
    blog_categories = BlogCategory.objects.all() # SELECT * FROM blogcategory
    return render(request, 'blog/category_list.html', {"categories": blog_categories})

def article_list(request, category_id):
    articles = Article.objects.filter(category_id=category_id) #by filter we can get several objects
    category = BlogCategory.objects.get(id=category_id) #by get we can get only one object
    breadcrumbs = {
        reverse('blog_category_list'): 'Blog',
        'current': category.name
    }
    return render(request, 'blog/article_list.html', {'articles': articles, 'category': category, 'breadcrumbs': breadcrumbs})

def article_view(request, category_id, article_id):
    category = BlogCategory.objects.get(id=category_id) #by get we can get only one object
    article = Article.objects.get(id=article_id)
    return render(request, 'blog/article_view.html', {'article': article, 'category': category})


def article_by_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    articles = Article.objects.filter(tags=tag)
    return render(request, 'blog/tag_list.html', {'tags': tag_id, 'articles': articles})







