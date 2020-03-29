from core.models import Tag, Ingredient
from recipe import serializers
from rest_framework import authentication, permissions
from rest_framework import viewsets, mixins


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Return objects only owned by authorized user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Save with owner name"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
