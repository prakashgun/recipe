from core.models import Tag, Ingredient
from recipe import serializers
from rest_framework import authentication, permissions
from rest_framework import viewsets, mixins


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
