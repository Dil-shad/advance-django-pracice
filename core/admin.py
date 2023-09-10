import pprint
from django.contrib.sessions.models import Session
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Contact, SellerAdditional, Seller, CustomerAdditional, CustomerManager, Customer, Product, Cart, ProductInCart,Order, Order,ProductInOrder,PremiumProduct

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),
        # ('Permissions', {
         #'fields': ('is_staff', 'is_active', 'is_superuser', )}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class SellerAdditionalInline(admin.TabularInline):
    model = SellerAdditional


class SellerAdmin(admin.ModelAdmin):
    inlines = (
        SellerAdditionalInline,
    )
class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer)
admin.site.register(SellerAdditional)
admin.site.register(CustomerAdditional)
admin.site.register(Product)
admin.site.register(PremiumProduct)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        ProductInOrderInline,
    )
    



class ProductInCartInline(admin.TabularInline):
    model = ProductInCart


class CartInline(admin.TabularInline):
    model = Cart  # onetoonefield foreignkey


@admin.register(Cart)  # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    # here user__is_staff will not work
    list_display = ('user', 'staff', 'created_on',)
    list_filter = ('user', 'created_on',)
    # fields = ('staff',)           # either fields or fieldset
    fieldsets = (
        # only direct relationship no nested relationship('__') ex. user__is_staff
        (None, {'fields': ('user', 'created_on',)}),
        # ('User', {'fields': ('staff',)}),
    )
    inlines = (
        ProductInCartInline,
    )
    # To display only in list_display

    def staff(self, obj):
        return obj.user.is_staff
    # staff.empty_value_display = '???'
    staff.admin_order_field = 'user__is_staff'  # Allows column order sorting
    staff.short_description = 'Staff User'  # Renames column head

    # Filtering on side - for some reason, this works
    # with direct foreign key(user) no error but not shown in filters, with function error
    list_filter = ['user__is_staff', 'created_on',]
    # ordering = ['user',]
    # with direct foreign key no error but filtering not possible directly
    search_fields = ['user__username']



# class Order(admin.ModelAdmin):
    

























# 1 using simple database for sessions

# If you remove this model admin below for sessions then you will see encrypted data only
# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return obj.get_decoded()
#     list_display = ['session_key', '_session_data', 'expire_date']
# admin.site.register(Session, SessionAdmin)

# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
#     _session_data.allow_tags=True
#     list_display = ['session_key', '_session_data', 'expire_date']
#     readonly_fields = ['_session_data']
#     exclude = ['session_data']
#     date_hierarchy='expire_date'


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']


admin.site.register(Session, SessionAdmin)

# admin.site.register(Session)
