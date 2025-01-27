from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from blogs.models import Blog
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import BlogPostSerializer, BlogSerializer, CommentSerializer
from rest_framework import status
from blogs.models import Comments
from blogs.utils import filter_blogs, paginate_response, handle_blog_post, send_email

# Create your views here.

class BlogAPI(APIView):
       permission_classes = [IsAuthenticated]
       authentication_classes = [TokenAuthentication]

       def get(self,request):
            blogs = Blog.objects.filter(status='published')  
            filtered_blogs = filter_blogs(blogs,request.query_params)

            response_data = paginate_response(filtered_blogs, request, BlogSerializer)
            return Response({'messsage' : "Blogs retrived successfully"}, response_data, status=status.HTTP_200_OK)

       def post(self, request):
        data = request.data
        author = self.request.user
        return handle_blog_post(data, author, BlogPostSerializer)
       
class BlogGetUpdateDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
            serializer = BlogSerializer(blog)
            return Response({'messsage' : "Blog retrived successfully"}, serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'error' : "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({'error' : "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        if self.request.user != blog.author:
            return Response({'error' : "permission denied"},status=status.HTTP_403_FORBIDDEN)
        else:
            blog.delete()
            return Response({'messsage' : "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
    def put(self,request,blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({'error' : "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        if self.request.user != blog.author:
                return Response({'error' : "permission denied"},status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = BlogPostSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message' : "Blog updated successfully"}, serializer.data, status=status.HTTP_200_OK)
            return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
       
class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        author = self.request.user
        serializer = CommentSerializer(data = data)

        if serializer.is_valid():
            serializer.save(author = author)
            send_email(self.request.user.email)
            return Response({'message' : "Comment added to the blog"}, serializer.data, status=status.HTTP_200_OK)
        return Response({'error' : serializer.errors}, serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CommentDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self,comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)

            if self.request.user != comment.author:
                return Response({'error' : "permission denied"},status=status.HTTP_403_FORBIDDEN)
        
            serializer = CommentSerializer(comment)
            comment.delete()
            return Response({'message' : "Comment deleted successfully"}, serializer.data ,status=status.HTTP_204_NO_CONTENT)

        except Comments.DoesNotExist:
            return Response({'error' : "Comment not found"},status=status.HTTP_404_NOT_FOUND)


