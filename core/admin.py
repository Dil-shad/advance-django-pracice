from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Contact,SellerAdditional,Seller,CustomerAdditional,CustomerManager,Customer
# Register your models here.



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'name','type', 'password')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', )}),   

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



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer)
admin.site.register(SellerAdditional)
admin.site.register(CustomerAdditional)
