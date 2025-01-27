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
            
            """
            Handles GET requests to retrieve published blogs.
            Args:
                Request: The HTTP request object containing query parameters.
            Returns:
                Response: A response object containing a paginated list of filtered blogs based on query params and a success message.
            """
            
            blogs = Blog.objects.filter(status='published')  
            filtered_blogs = filter_blogs(blogs,request.query_params)

            response_data = paginate_response(filtered_blogs, request, BlogSerializer)
            return Response({'messsage' : "Blogs retrived successfully"}, response_data, status=status.HTTP_200_OK)

       def post(self, request):
        """
        Handle POST request to create a new blog post.
        Args:
            request (Request): The HTTP request object containing the data for the new blog post.
        Returns:
            Response: The response object after handling the blog post creation.
        """
        data = request.data
        author = self.request.user
        return handle_blog_post(data, author, BlogPostSerializer)
       
class BlogGetUpdateDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,blog_id):
        """
        Retrieve a blog by its ID.
        Args:
            blog_id (int): The ID of the blog to retrieve.
        Returns:
            Response: A Response object containing the serialized blog data and a success message if the blog is found,
                      or an error message if the blog does not exist.
        """
        try:
            blog = Blog.objects.get(pk=blog_id)
            serializer = BlogSerializer(blog)
            return Response({'messsage' : "Blog retrived successfully"}, serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'error' : "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,blog_id):
        """
        Delete a blog post.
        Args:
            blog_id (int): The ID of the blog post to delete.
        Returns:
            Response:
                - 404 Not Found: If the blog post does not exist.
                - 403 Forbidden: If the user is not the author of the blog post.
                - 204 No Content: If the blog post is successfully deleted.
        """
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
        """
        Update an existing blog post.
        Args:
            request (Request): The HTTP request object containing the data to update the blog post.
            blog_id (int): The ID of the blog post to be updated.
        Returns:
            Response:
                - 200 OK: If the blog post is successfully updated.
                - 400 Bad Request: If the provided data is invalid.
                - 403 Forbidden: If the requesting user is not the author of the blog post.
                - 404 Not Found: If the blog post does not exist.
        """
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
        """
        Handle POST request to add a comment to a blog post.
        Args:
            request (Request): The HTTP request object containing the comment data.
        Returns:
            Response: Success message  if the comment is valid,
                      An error message if the comment is invalid.
        Side Effects:
            Sends an email notification to the author of the comment upon successful addition of the comment.
        """
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
        """
        Deletes a comment with the given comment_id.
        Args:
            comment_id (int): The ID of the comment to be deleted.
        Returns:
            Response:
                - 204 NO CONTENT: If the comment is successfully deleted.
                - 404 NOT FOUND: If the comment does not exist.
                - 403 FORBIDDEN: If the user is not the author of the comment.
        """
        try:
            comment = Comments.objects.get(id=comment_id)

            if self.request.user != comment.author:
                return Response({'error' : "permission denied"},status=status.HTTP_403_FORBIDDEN)
        
            serializer = CommentSerializer(comment)
            comment.delete()
            return Response({'message' : "Comment deleted successfully"}, serializer.data ,status=status.HTTP_204_NO_CONTENT)

        except Comments.DoesNotExist:
            return Response({'error' : "Comment not found"},status=status.HTTP_404_NOT_FOUND)


