from logging import raiseExceptions

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from apps.blog.models import Article, Tag
from apps.api.blog.serializer import ArticleWriteSerializer, ArticleReadSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleReadSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        queryset = Article.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        user = self.request.query_params.get('category')

        if user:
            queryset = queryset.filter(user=user)

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ArticleWriteSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permission() for permission in [permissions.IsAdminUser]]
        return [permission() for permission in [permissions.IsAdminUser]]

    # Creating separate function to follow DRY rule
    # Using static method to use it(check_tags) without self
    @staticmethod
    def check_tags(tags_list):
        tags = []
        for tag_name in tags_list:
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                tag = Tag.objects.create(name=tag_name)
            tags.append(tag)
        return tags

    def save_model(self, request, serializer):
        tags = self.check_tags(serializer.validated_data.get('tags'))
        article = serializer.save(user=self.request.user, tags=tags)
        read_serializer = self.serializer_class(article, context={'request': request})
        return read_serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Receiving necessary serializer
        serializer.is_valid(raise_exception=True)
        read_serializer = self.save_model(request, serializer)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Receiving an id '.../article/2/'
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        read_serializer = self.save_model(request, serializer)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
