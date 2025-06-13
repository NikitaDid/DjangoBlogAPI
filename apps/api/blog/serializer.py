from rest_framework import serializers
from apps.blog.models import Article, BlogCategory, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'name', 'image')

# for create, update, delete methods
class ArticleWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=64))

    class Meta:
        model = Article
        fields = (
            'id',
            'category',
            'image',
            'title',
            'text_preview',
            'text',
            'publish_date',
            'tags',
        )


# for read method
class ArticleReadSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'category',
            'user',
            'title',
            'text_preview',
            'text',
            'publish_date',
            'image',
            # 'image_thumbnail',
            'created_at',
            'tags'
        )





