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
    brand=models.CharField(max_length=100)
    date_added=models.DateTimeField(default=timezone.now)

    
    # class Meta:
    #     ordering = ['-price']
        
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
        
        

class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices = status_choices, default=1)

    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " " + str(self.id)
    
    
    
class ProductInOrder(models.Model):
   
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = (('order', 'product'),)
        
        
        
    
    
    
class PremiumProduct(models.Model):
    product_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to = "premiumproductimages", default = None, null = True, blank = True)
    price = models.FloatField()
    brand = models.CharField(max_length=1000)
    date_added = models.DateTimeField(default=timezone.now)

    # custom permissions dependent to a specific model
    class Meta:
        permissions = (
            ('can_avail_premium_delivery', 'can avail for premium delivery on premium products'),
            ('can_add_premium_discount', 'can avail more premium discount on premium products')
       )



class CustomPermissions(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.

        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        # All the custom permissions not related to models on Manufacturer
        permissions = (
            ('accept_order', 'can accept order'),
            ('reject_order', 'can reject order'),
            ('view_order', 'can view order'),
            ('change_order', 'can change order'),
            ('view_return', 'can view return'),
            ('accept_return', 'can accept return'),
            ('reject_return', 'can reject return'),
            ('change_return', 'can change return'),
            ('view_dashboard', 'can view dashboard'),
        )
