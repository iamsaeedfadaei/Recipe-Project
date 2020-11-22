from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """serializer for ingredients objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)



class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipe objects."""
    # ingredients and tags are kind of foreignkeys so we should use PrimaryKeyRelatedField in serializers for them.
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes',
                  'price', 'link'
                  )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """serializer for a recipe detail"""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
