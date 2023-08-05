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




#1 using simple database for sessions 
from django.contrib.sessions.models import Session
import pprint

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
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']

admin.site.register(Session, SessionAdmin)

#admin.site.register(Session)
