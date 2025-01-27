from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from blogs.models import Blog
from rest_framework.response import Response

def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  
        recipient_list,  
        fail_silently=False,  
    )

def send_email(email):
    subject = "New comment added to your article"
    message = "New comment added to your article"
    recipient_list = [email]  
    send_notification_email(subject, message, recipient_list)

def filter_blogs(queryset, query_params):
    
    author = query_params.get('author')
    if author:
        queryset = queryset.filter(author=author)

    category = query_params.get('category')
    if category:
        queryset = queryset.filter(category=category)

    tags = query_params.getlist('tags')
    if tags:
        for tag in tags:
            queryset = queryset.filter(tags__name=tag)

    search_query = query_params.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(blog_content__icontains=search_query) |
            Q(tags__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()

    return queryset


def paginate_response(queryset, request, serializer_class):
    
    paginator = PageNumberPagination()
    paginator.page_size = 2
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(paginated_queryset, many=True)

    return {
        "success": True,
        "message": "Data retrieved successfully.",
        "count": paginator.page.paginator.count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "data": serializer.data,
    }

def handle_blog_post(data, author, serializer_class):
    blog_status = data.get('status')

    if blog_status == 'publish':
        blog_id = data.get('id')

        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        blog.status = 'publish'
        blog.save()

        return Response({'message': "Blog published"}, status=status.HTTP_200_OK)
    else:
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response({'message': "Blog saved as draft"}, serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

