from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.utils import get_and_send_confirmation_code
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (IsAdmin, IsAdminSuperuser,
                          IsAuthorModeratorAdminSuperuserOrReadOnly, ReadOnly)
from .serializers import (CategotySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          UserAdminSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminSuperuser,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username',)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            serializer_class=UserSerializer,
            pagination_class=None,
            queryset=User.objects.all())
    def me(self, request):
        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.data.get('username') and request.data.get('email'):
        user = User.objects.filter(username=request.data.get('username'),
                                   email=request.data.get('email'))
        if user.exists():
            get_and_send_confirmation_code(user)
            return Response(request.data, status=status.HTTP_200_OK)
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.filter(**serializer.data)
    get_and_send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if serializer.validated_data[
            'confirmation_code'] == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        'Проверьте правильность указанных для получения токена данных.',
        status=status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly,
                          IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.kwargs.get('title_id')
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly,
                          IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )


class GenreViewSet(ModelMixinSet):
    """Получить список всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = (GenreSerializer)
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(ModelMixinSet):
    """Получить список всех категорий. Права доступа: Доступно без токена."""
    queryset = Category.objects.all()
    serializer_class = (CategotySerializer)
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список всех объектов."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = (TitleSerializer)
    permission_classes = (IsAdmin,)
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCreateSerializer
