from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def get_rating_by_article_pk(pk):
    rating = Rating.objects.filter(article=pk).aggregate(
        Sum('rating_change')
    )['rating_change__sum']
    if rating:
        return rating
    else:
        return 0


class ArticleSerializer(serializers.ModelSerializer):
    rubric_url = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'rubric_url', 'image', 'content', 'characters', 'created', 'rating')

    def get_rubric_url(self, article_object):

        super_rubrics = SuperRubric.objects.filter(pk=article_object.rubric.super_rubric.id).values('slug')
        super_rubrics_slug = super_rubrics[0]['slug']

        rubrics = Rubric.objects.filter(pk=article_object.rubric.id).values('slug')
        rubrics_slug = rubrics[0]['slug']

        slugs = super_rubrics_slug + '/' + rubrics_slug
        return slugs

    def get_rating(self, article_object):
        return get_rating_by_article_pk(article_object.pk)


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    ais = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'rubric', 'title', 'content', 'characters', 'author',
                  'source', 'created', 'image', 'rating', 'comments', 'ais')

    def get_comments(self, article):
        comments = Comment.objects.filter(article=article.pk)
        comment_serializer = CommentSerializer(comments, many=True)
        return comment_serializer.data

    def get_rating(self, article):
       return get_rating_by_article_pk(article.pk)

    def get_ais(self, article):
        ais = AdditionalImage.objects.filter(article=article.pk)
        ais_serializer = AISerializer(ais, many=True, context={'request': self.context['request']})
        return ais_serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, comment):
        return get_object_or_404(GrUser, pk=comment.author_id).username

    class Meta:
        model = Comment
        fields = ('author', 'content', 'created')


class AISerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalImage
        fields = ('image', 'caption')


class RubricListSerializer(serializers.ModelSerializer):
    rubric_url = serializers.SerializerMethodField()
    super_name = serializers.SerializerMethodField()

    class Meta:
        model = Rubric
        fields = ('name', 'super_name', 'rubric_url')

    def get_rubric_url(self, rubric_object):
        super_rubric = SuperRubric.objects.filter(pk=rubric_object.super_rubric_id).values('slug')
        super_rubric_slug = super_rubric.first()['slug']
        return super_rubric_slug + '/' + rubric_object.slug

    def get_super_name(self, rubric_object):
        super_rubric = SuperRubric.objects.filter(pk=rubric_object.super_rubric_id).values('name')
        super_name = super_rubric.first()['name']
        return super_name
