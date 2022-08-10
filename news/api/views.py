from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from news.models import Article, Journalist
from .serializers import ArticleSerializer, JournalistSerializer


# Function based views
# @api_view(["GET", "POST"])
# def article_list_create_api_view(request):
#     if request.method == "GET":
#         articles = Article.objects.filter(is_active=True)
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def article_detail_api_view(request, pk):
#     try:
#         articles = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response({'code': 404, 'message': 'Article not found!'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = ArticleSerializer(articles)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         articles.is_active = False
#         articles.save()
#         return Response({'code': 204, 'message': "Successfully delete the article!"},\
#         status=status.HTTP_204_NO_CONTENT)
#     elif request.method == "PUT":
#         serializer = ArticleSerializer(instance=articles, data=request.data)
#         if serializer.is_valid():
#             serializer.update(instance=articles, validated_data=request.data)
#             return Response({serializer.data}, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# Class based views
class JournalistListCreateView(APIView):
    def get(self, request):
        try:
            author = Journalist.objects.all()
        except Journalist.DoesNotExist:
            return Response({'code': 404, 'message': 'Journalist not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JournalistSerializer(author, many=True, context={
            'request': request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListCreateView(APIView):
    def get(self, request):
        try:
            articles = Article.objects.filter(is_active=True)
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': 'Article not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        articles = get_object_or_404(Article, id=pk)
        return articles

    def get(self, request, pk):
        object_query = self.get_object(pk)
        serializer = ArticleSerializer(object_query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        object_query = self.get_object(pk)
        object_query.is_active = False
        object_query.save()
        return Response({'code': 204, 'message': "Successfully delete the article!"}, status=status.HTTP_204_NO_CONTENT)
