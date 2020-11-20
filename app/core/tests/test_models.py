from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models



def sample_user(email='test@gmail.com', password='test1234'):
    """create a sample user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ testing creation of new user with email is successful"""
        email = 'test@gmail.com'
        password = 'testpassword1234'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    

    def test_new_user_email_normalized(self):
        """testing email of the new user is normalized."""
        email = 'test@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')
    
    def test_create_new_superuser(self):
        """testing creation of new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test1234',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    
    def test_tag_str(self):
        """test the tag string representation."""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan',
        ) 
        self.assertEqual(str(tag), tag.name)

    
    def test_ingredient_str(self):
        """ test the ingredient string representation."""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)


    def test_recipe_str(self):
        """test the recipe string represetation"""
        """creating  recipe new object and than we can successfully retrieve it."""
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak & Mushroom Sauce',
            time_minutes = 5,
            price = 5.00
        )
        self.assertEqual(str(recipe), recipe.title)
