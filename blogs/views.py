from rest_framework.decorators import APIView
from rest_framework.response import Response
from blogs.models import Blog
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import BlogPostSerializer, BlogSerializer, CommentSerializer
from rest_framework import status


# Create your views here.

class BlogAPI(APIView):
       permission_classes = [IsAuthenticated]
       authentication_classes = [TokenAuthentication]

       def get(sel,request):
           blogs = BlogSerializer(Blog.objects.all(), many = True).data
           return Response(blogs)

       def post(self, request):
        data = request.data
        author = self.request.user
        serializer = BlogPostSerializer(data = data)
        if serializer.is_valid():
            serializer.save(author = author)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       

