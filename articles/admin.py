from django.contrib import admin

from .models import *


class RubricInline(admin.TabularInline):
    model = Rubric
    fk_name = 'super_rubric'


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (RubricInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    list_display = ('image', 'caption')
    max_num = 3


class CommentInline(admin.TabularInline):
    model = Comment
    list_display = ('author', 'content')
    max_num = 1


class RatingInline(admin.TabularInline):
    model = Rating
    list_display = ('user', 'rating_change')
    max_num = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rubric', 'author')
    fields = (
        ('rubric', 'author'),
        'title', 'content', 'characters', 'source', 'image', 'is_active', 'created'
    )
    inlines = (AdditionalImageInline, CommentInline,RatingInline,)
    readonly_fields = ('created',)


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = (
        ('article', 'author', 'created'),
        'content',
        'is_approved',
    )
    readonly_fields = ('article', 'author', 'created', 'content',)


admin.site.register(Comment, CommentAdmin)
