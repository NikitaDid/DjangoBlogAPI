from django.urls import path, include

from apps.api.blog.views import ArticleViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
router.register('article/image', ArticleViewSet, basename='article_image')

urlpatterns += router.urls

# router = DefaultRouter
# router.register('article', ArticleViewSet, basename='article')
#
#
# urlpatterns = [
#     path('api/', include(router.urls)),
# ]