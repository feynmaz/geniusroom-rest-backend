from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination
    queryset = Article.objects.all()


class ArticlesLiked(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.request.user.id
        article_ids = Rating.objects.filter(user_id=user_id, rating_change=1).values('article_id')
        return Article.objects.filter(pk__in=article_ids)


class ArticleByRubricListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        rubric_slug = self.kwargs['rubric_slug']
        rubric_id = Rubric.objects.filter(slug=rubric_slug).values('id')[0]['id']
        return Article.objects.filter(rubric_id=rubric_id)


class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer

    def get_queryset(self):
        article = Article.objects.filter(pk=self.kwargs.get('pk'))
        return article

    def get_serializer_context(self):
        context = super(ArticleDetailView, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class RubricView(generics.ListAPIView):
    pagination_class = None
    serializer_class = RubricListSerializer
    queryset = Rubric.objects.all().order_by('super_rubric__id', 'id')


@authentication_classes([IsAuthenticated])
@api_view(http_method_names=['POST'])
def create_comment(request, pk):
    data = {
        'content': request.data.get('content'),
        'author': request.user.pk,
        'article': pk
    }
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RatingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        rating_change = request.data.get('rating_change')

        rating_record, created = Rating.objects.update_or_create(
            article=get_object_or_404(Article, pk=kwargs['pk']),
            user=request.user,
            defaults={'rating_change': rating_change}
        )

        body = {
            'rating': get_rating_by_article_pk(kwargs['pk'])
        }
        return Response(body, status=HTTP_200_OK)


@authentication_classes([IsAuthenticated])
@api_view(http_method_names=['GET'])
def user_rating(request, pk):
    rating = Rating.objects.filter(user=request.user.pk, article=pk)
    rating_change = rating[0].rating_change if rating.count() != 0 else 0

    return Response({
        'rating_change': rating_change
    })








