from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from .managers  import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models import Q



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


# Model Managers for proxy models
class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=CustomUser.Types.SELLER))

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=CustomUser.Types.CUSTOMER))




# Model Managers for proxy models
# ... (Same as before)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"

    default_type = Types.CUSTOMER
    type = MultiSelectField(choices=Types.choices, max_length=100, default=[], null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)


    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_users'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users_permissions'
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)



class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,unique=True)
    gst = models.CharField(max_length=10)
    warehouse_location = models.CharField(max_length=1000)
    
    
    
    def __str__(self):
        return self.user.email
    


class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()

    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class Customer(CustomUser):
    default_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=5)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number should be exactly 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    query = models.TextField()





# ----------------------------------------------------------------#

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to = "core/productimages", default = None, null = True, blank = True)
    price = models.FloatField()

    @classmethod
    def updateprice(cls,product_id, price):
        product = cls.objects.filter(product_id = product_id)
        product = product.first()
        product.price = price
        product.save()
        return product

    @classmethod
    def create(cls, product_name, price):
        product = Product(product_name = product_name, price = price)
        product.save()
        return product
    
    def __str__(self):
        return self.product_name
    
    
    
    

class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user = user)
        # you can perform more operations 
        return cart

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    objects = CartManager()

class ProductInCart(models.Model):
    
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    class Meta:
        unique_together = (('cart', 'product'),)
        
        
