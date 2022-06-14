from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
LOGIN_URL = reverse('user:login')
PROFILE_URL = reverse('user:myprofile')


def create_user(**kwargs):
    return get_user_model().objects.create_user(
        email=kwargs.get('email',"defaulttest@sns.com"),
        password=kwargs.get('password',"DefTest@123"),
        name=kwargs.get('name',"Sns Default User"),
        mobile=kwargs.get('mobile',"+1999999999"),
        address=kwargs.get('address',"Address default user"),
        city=kwargs.get('city',"Default city"),
        pincode=kwargs.get('pincode',"A1B 2D3")
    )

def get_sample_payload(**kwargs):
    return { 
        "email": kwargs.get('email',"defaulttest@sns.com"),
        "password": kwargs.get('password',"DefTest@123"),
        "name": kwargs.get('name',"Sns Default User"),
        "mobile": kwargs.get('mobile',"+1999999999"),
        "address": kwargs.get('address',"Address default user"),
        "city": kwargs.get('city',"Default city"),
        "pincode": kwargs.get('pincode',"A1B 2D3")
    }


class PublicUserApiTest(TestCase):
    """Test the users public API's"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        res = self.client.post(CREATE_USER_URL, get_sample_payload(password='supersecret'))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password('supersecret'))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Test creating user that already exists"""
        create_user(email='test@sns.com')
        res = self.client.post(CREATE_USER_URL, get_sample_payload(email='test@sns.com'))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 chars"""
        res = self.client.post(CREATE_USER_URL, get_sample_payload(email='test@sns.com', 
                                                                    password='tes'))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email='test@sns.com'
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test a token is created for user"""
        create_user(email='test@django.com', password='test@123')
        res = self.client.post(LOGIN_URL, get_sample_payload(email='test@django.com', 
                                                                password='test@123'))
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Token is not created if invalid credentials are given"""
        create_user(email='test@django.com', password='test@123')
        res = self.client.post(LOGIN_URL, get_sample_payload(email='test@django.com', password='wrngpwd@123'))

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Token is not created if user does not exists"""
        res = self.client.post(LOGIN_URL, get_sample_payload(email='InvalidUser@django.com', password='test@123'))

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_field(self):
        """Test email and password are required"""
        res = self.client.post(LOGIN_URL, get_sample_payload(email='InvalidUser@django.com', password=''))

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for user"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API tests that require authentication"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
            'mobile': self.user.mobile,
            'address': self.user.address,
            'city': self.user.city,
            'pincode': self.user.pincode,
            'is_staff': False
        })

    def test_post_not_allowed(self):
        """Test that POST is not allowed on myprofile urls"""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'password': 'testmod@123',
            'name': 'Test mod name'
        }
        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
