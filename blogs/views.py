from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from blogs.models import Blog
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import BlogPostSerializer, BlogSerializer, CommentSerializer
from rest_framework import status
from blogs.models import Comments
from blogs.utils import send_notification_email


# Create your views here.

class BlogAPI(APIView):
       permission_classes = [IsAuthenticated]
       authentication_classes = [TokenAuthentication]

       def get(self,request):
            blogs = Blog.objects.all()  

            author = request.query_params.get('author')
            category = request.query_params.get('category')
            tags = request.query_params.get('tags') 

            if author:
                blogs = blogs.filter(author=author)
            if category:
                blogs = blogs.filter(category=category)
            if tags:
                for tag in tags:
                    blogs = blogs.filter(tags=tag)

            search_query = request.query_params.get('search')
            if search_query:
                blogs = blogs.filter(
                    Q(title__icontains=search_query) |
                    Q(blog_content__icontains=search_query) |
                    Q(tags__tag__icontains=search_query) |
                    Q(category__category__icontains=search_query)
                ).distinct()
       
            paginator = PageNumberPagination()  
            paginator.page_size = 2
            paginated_blogs = paginator.paginate_queryset(blogs, request)  
            serializer = BlogSerializer(paginated_blogs, many=True)  
            return paginator.get_paginated_response(serializer.data)  

       def post(self, request):
        data = request.data
        author = self.request.user
        serializer = BlogPostSerializer(data = data)
        if serializer.is_valid():
            serializer.save(author = author)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       

class BlogGetUpdateDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
            if request.user != blog.author:
                return Response(
                    {"permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
            else :
                blog.delete()
                return Response({"Blog deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
                
        except Blog.DoesNotExist:
            return Response({"Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({"Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != blog.author:
                return Response(
                    {"permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            serializer = BlogPostSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        author = self.request.user
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save(author = author)
            subject = "New comment added to your article"
            message = "New comment added to your article"
            recipient_list = [self.request.user.email]  
            send_notification_email(subject, message, recipient_list)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CommentDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self,request,comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)

            if request.user != comment.author:
                return Response(
                    {"permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data = CommentSerializer(comment).data

            comment.delete()
            return Response(
                {"message": "Comment deleted successfully.", "comment": data},
                status=status.HTTP_204_NO_CONTENT
            )

        except Comments.DoesNotExist:
            return Response(
                {"Comment not found."},
                status=status.HTTP_404_NOT_FOUND
            )


