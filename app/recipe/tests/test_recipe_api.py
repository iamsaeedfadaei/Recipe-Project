from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer



RECIPE_URL = reverse('recipe:recipe-list')

def deatil_url(recipe_id):
    """return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='Main course'):
    """create and return a sample tag."""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """create and return a sample object."""
    return Ingredient.objects.create(user=user, name=name)



def sample_recipe(user, **params):
    """create and return a sampel recipe."""
    """ ** in **params means that any additional parameter to the user that passed in will get passed to a dictionary called params."""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)  #update function will accept a dictionary object and wichever keys in dictionary and will update them but if dit does not exist it will create them.

    return Recipe.objects.create(user=user, **defaults)  # actually ** has reverse effect === dictionary to arguments and arguments to dictionary.


class PublicRecipeApiTests(TestCase):
    """test unauthorized recipe API access."""

    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        """test authentication is rquired."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """test authenticated recipe API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
            """Test retrieving list of recipes"""
            sample_recipe(user=self.user)
            sample_recipe(user=self.user)

            res = self.client.get(RECIPE_URL)

            recipes = Recipe.objects.all().order_by('-id')
            serializer = RecipeSerializer(recipes, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """test retrieving recipes for users."""
        user2 =get_user_model().objects.create_user(
            'other@gmail.com',
            'other1234'
        )
        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
        

    def test_view_recipe_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))  #this is how we add to manytomany field
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = deatil_url(recipe.id)
        res= self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)  #this is a single object not many=True :)
        self.assertEqual(res.data, serializer.data)


    def test_create_basic_recipe(self):
        """test creating recipe."""
        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 10,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])   #when we call get on an object it will return a dictionary of that object.
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))   
            #getattr is allowing us to retrieve an attribute from an object. we can't use recipe.key cause for python it looks like recipe has a key attribute but it does not.
        
    
    def test_create_recipe_tags_self(self):
        """test creating recipe with tags."""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')
        payload = {
            'title': 'Avocado lime cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)  #assertIn will check the tag1 is in tags or not!
        self.assertIn(tag2, tags)


    def test_create_recipe_with_ingredients(self):
        """create user with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')

        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00
        }

        res =self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
