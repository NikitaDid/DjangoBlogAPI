from django.shortcuts import render, redirect
from django.urls import reverse

from apps.blog.forms import CommentForm
from apps.blog.models import BlogCategory, Article, Tag, Comment


def blog_category_list(request):
    blog_categories = BlogCategory.objects.all()  # SELECT * FROM blogcategory
    return render(request, 'blog/category_list.html', {"categories": blog_categories})


def article_list(request, category_id):
    articles = Article.objects.filter(category_id=category_id)  # by filter we can get several objects
    category = BlogCategory.objects.get(id=category_id)  # by get we can get only one object
    breadcrumbs = {
        reverse('blog_category_list'): 'Blog',
        'current': category.name
    }
    return render(request, 'blog/article_list.html',
                  {'articles': articles, 'category': category, 'breadcrumbs': breadcrumbs})


def article_view(request, category_id, article_id):
    category = BlogCategory.objects.get(id=category_id)  # by get we can get only one object
    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(article=article, is_checked=True)
    return render(request, 'blog/article_view.html', {'article': article, 'category': category, 'comments':comments})


def article_by_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    articles = Article.objects.filter(tags=tag)
    return render(request, 'blog/tag_list.html', {'tags': tag_id, 'articles': articles})


# def comment_view(request, article_id, category_id):
#     article = Article.objects.get(id=article_id)
#     print(f"--- Отладка comment_view для article_id: {article_id} ---")
#     print(f"Запрос метод: {request.method}")
#     comments = Comment.objects.filter(article=article).order_by('-publish_date')
#     for comment in comments:
#         print(
#             f"Комментарий ID: {comment.id}, Автор: {comment.name if comment.name else (comment.user.username if comment.user else 'Гость')}, Текст: {comment.text[:30]}...")  # Выводим часть текста для наглядности
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.article = article #connecting comment to article
#             if request.user.is_authenticated:
#                 comment.user = request.user
#                 comment.email = request.user.email
#             comment.save()
#             print('makuin')
#             return redirect('blog_article_view',category_id=category_id, article_id=article.id)
#         else:
#             print('Matter')
#             return render(request, 'blog/article_view.html', {'article': article, 'form': form, 'comments': comments})
#     else:
#         print("Получен GET запрос на comment_view - это, возможно, нежелательно.")
#         return redirect('blog_article_view', category_id=category_id, article_id=article.id)

def create_comment(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        data = request.POST.copy()
        data.update(article=article_id)  # Подставляем статью

        if not request.user.is_anonymous:  # if anonymous, then better to use is_anonymous, than is_authenticated
            user = request.user
            data.update({
                'name': f"{user.last_name} {user.first_name}",
                "is_checked": True,
                "email": user.email,
                "user": user})

        request.POST = data
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            breadcrumbs = {'current': "Comment was successfully added"}
            return render(request, 'blog/comment_created.html', {
                "comment": comment,
                "breadcrumbs": breadcrumbs,
                "article": article
            })
        else:
            print(form.errors)
