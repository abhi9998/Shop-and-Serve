from django.core.exceptions import ValidationError
from django.test import TestCase
# Get user model helper function
from django.contrib.auth import get_user_model


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

class SnsUserModelTest(TestCase):

    def test_create_user_successful(self):
        """Test creating a new user with email"""
        email='test@sns.com'
        password='Test@123'
        name = 'Sns Test User'
        mobile = '+1999999998',
        address = 'Address test user'
        city = 'Test city'
        pincode = 'A1B 2C3'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
            mobile=mobile,
            address=address,
            city=city,
            pincode=pincode
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, name)
        self.assertEqual(user.mobile, mobile)
        self.assertEqual(user.address, address)
        self.assertEqual(user.city, city)
        self.assertEqual(user.pincode, pincode)
        self.assertEqual(user.walletamount, 0.00)
        self.assertEqual(user.verifystatus, 'pending')

    def test_new_user_email_normalized(self):
        """Test email for new user is normalized"""
        email='test@SNS.com'
        user = create_user(email=email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):       
            create_user(email=None)
    
    def test_invalid_pincode(self):
        """Test creating user with invalid pincode raises error"""      
        user = create_user(pincode='A1B2C3')
        with self.assertRaises(ValidationError):
            if user.full_clean():
                user.save()
        self.assertEqual(get_user_model().objects.filter(email='test@SNS.com').count(), 0)

    def test_invalid_phone(self):
        """Test creating user with invalid phone raises error"""        
        user = create_user(mobile='9999')
        with self.assertRaises(ValidationError):
            if user.full_clean():
                user.save()
        self.assertEqual(get_user_model().objects.filter(email='test@SNS.com').count(), 0)
