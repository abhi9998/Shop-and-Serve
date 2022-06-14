from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for User profiles"""

    def create_user(self, email, name, mobile, address, city, pincode, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            mobile=mobile,
            address=address,
            city=city,
            pincode=pincode,
            **extra_fields
        )
        user.set_password(password) # Django encodes the password to save the sensitive data
        user.save(using=self._db)

        return user

    # TODO: Check super user
    def create_superuser(self, email, name, pincode, mobile, city, password=None):
        """Creates and saves new super user"""
        user = self.create_user(email, name, pincode, mobile, city, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class SnsUser(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    class Meta:
        db_table = "snsuser"
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Custom model fields
    name = models.CharField(max_length=30)
    mobile_regex = RegexValidator(regex=r'^\+?1?[0-9]{9,15}$',
                message="Phone number must be entered in the format: '+199999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[mobile_regex], max_length=17, unique=True) # validators should be a list
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    verifystatus = models.CharField(max_length=30, default='pending')
    walletamount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    registeredat = models.DateTimeField(auto_now_add=True)
    pincode_regexp = RegexValidator(regex=r'^[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9]$',
                message="Pincode must be entered in format 'A3B 5HG'.")
    pincode = models.CharField(validators=[pincode_regexp], max_length=7)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'address', 'city', 'pincode']


class Group(models.Model):
    """Database model for the community groups"""
    class Meta:
        db_table = "group"

    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, default='private')
    description = models.CharField(max_length=150)
    city = models.CharField(max_length=30)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """Bridge table for many to many mapping between a User and associated community groups"""
    class Meta:
        db_table = "groupmembership"

    userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    groupid = models.ForeignKey(Group, to_field='id', on_delete=models.CASCADE)
    isadmin = models.BooleanField(default=False)
