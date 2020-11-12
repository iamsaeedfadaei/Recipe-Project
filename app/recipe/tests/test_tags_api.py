from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """test the public ly available tags api."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test login is required for retrieving tags."""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTagsApiTests(TestCase):
    """Test authorized user tag api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test1234',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    
    def test_retrieve_tags(self):
        """test retieving tags."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        res = self.client.get(TAGS_URL)
        tags =Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)  #we use many because it would be list of items not just a single one.

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)
        

    def test_tags_limited_to_user(self):
        """test the tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
        'test2@gmail.com',
        'test21234',
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)


    def test_create_tag_successful(self):
        """Test create tag."""
        payload = {
            'name': 'Test tag',
        }
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user = self.user,
            name = payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test creating a tag with invalid data"""
        payload={'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)