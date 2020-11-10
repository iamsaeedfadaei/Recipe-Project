from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient  #for have a built in tester client
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')   #for editing profile



def create_user(**params):  # **params meaning a dynamic list that can be changed.
    """ a helper function for creating user to prevent adding user manually."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test user api (public) because it doesnt need authenticated like password related authentication process."""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test creating user with valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test1234',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_exists(self):
        """ test creating an already exists user failure."""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test1234',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """test password must be more than 5 chars."""
        payload = {
            'email': 'test@gmail.com',
            'password': 'password',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        #making sure the user with this password cant be created:
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """test that a token is created for the user."""
        payload = {'email': 'test@gmail.com', 'password': 'test1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """test that token is not created with invalid credentials that given."""
        create_user(
            email = 'test@gmail.com',
            password = 'test1234',
        )
        payload = { 'email': 'test@gmail.com', 'password': 'wrongpassword'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_no_user(self):
        """test that token is not created if user does not exist."""
        payload = {'email': 'test@gmail.com', 'password':'test1234'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_missing_field(self):
        """test that  required fields would not be missing"""
        res = self.client.post(TOKEN_URL , {'eamil': 'test@gmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retieve_user_unauthorized(self):
        """ test that authentication is required for the users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """ test api userthat require authentication."""

    def setUp(self):
        self.user = create_user(
            email = 'test@gmail.com',
            password = 'test1234',
            name = 'name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)   # we use this useful helper function for forcing authentication.


    def test_retrieve_profile_success(self):
        """ test retrieving profile for logged in users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data , {
            'name' : self.user.name, 
            'email' : self.user.email,
        })   # somehow we exclude password field in retrieving user object.


    def test_post_me_not_allowed(self):
        """test that POST is not allowed in me_url."""
        res= self.client.post(ME_URL, {})   #pot request will send something in dictionary.
        self.assertEqual(res.status_code , status.HTTP_405_METHOD_NOT_ALLOWED)

    
    def test_update_user_profile(self):
        """ test updating the user profile for authenticated user."""
        payload = {
            'name': 'newname',
            'password': 'newtest1234',
            }
        # we use get for retrieving and post for creating and put & patch for editing api.(we use patch for updating the field we want and put for enitre object)
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()  #this helper function will update the db after editing it.
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


#     def test_retrieve_user_unauthorized(self):
#         """Test that authentication required for users"""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateUserApiTests(TestCase):
#     """Test API requests that require authentication"""

#     def setUp(self):
#         self.user = create_user(
#             email='test@londonappdev.com',
#             password='testpass',
#             name='fname',
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in user"""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'name': self.user.name,
#             'email': self.user.email,
#         })

#     def test_post_me_not_allowed(self):
#         """Test that POST is not allowed on the me URL"""
#         res = self.client.post(ME_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_update_user_profile(self):
#         """Test updating the user profile for authenticated user"""
#         payload = {'name': 'newname', 'password': 'newpassword123'}

#         res = self.client.patch(ME_URL, payload)

#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertTrue(self.user.check_password(payload['password']))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)


"""
setUP method:
The methods setUp and tearDown come from the base class unittest.TestCase.
These 2 methods are called at the beginning and at the end of the execution of a TestCase instance(and it only executes one single test method, remember?).
Implementing setUp and tearDown is equivalent to repeat the same code at the beginning and at the end of each test methods. 
Hence, you can consider them as a tool to avoid repetitive code in your tests.
setUp method will be run for each test!
"""
