from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email= 'admin@gmail.com',
            password = 'test1234',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            name = 'name',
            email = 'test@gmail.com',
            password = 'test1234',
        )

    def test_users_listed(self):
        """ testing that users are listed in user page."""
        url = reverse('admin:core_user_changelist') #this urls are django admin documentaion
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """testing user edit page is working."""
        url = reverse('admin:core_user_change', args=[self.user.id])   #admin/core/user/id
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """testing creating user page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
