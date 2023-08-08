from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Index.as_view(), name="index"),
    path("contactusclass", views.ContactUs.as_view(), name="contactusclass"),
    path("contactus", views.Contactus, name="contactus"),
    path("contactus2", views.contactus2, name="contactus2"),

    # Authentication Endpoints
    path('signup/', views.RegisterView.as_view(), name="signup"),
    # path('signupseller/', views.RegisterViewSeller.as_view(), name="signupseller"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('example', views.example_view, name="example"),
    path('testsession',views.testsession, name="testsession"),
    
    #Products
    
    #path('listproducts/', views.ProductListView.as_view(), name="listproducts"),
    path('listproducts/', views.listProducts, name="listproducts"),
    path('productdeatil/<int:pk>', views.ProductDetailView.as_view(), name="productdeatil"),
    path('addtocart/<int:id>/', views.addToCart, name="addtocart"),
    path('displaycart/', views.DisplayCart.as_view(), name="displaycart"),
    path('updatecart/<int:pk>/', views.UpdateCart.as_view(), name="updatecart"),
    path('deletefromcart/<int:pk>/', views.DeleteFromCart.as_view(), name="deletefromcart"),
    
    #search autocomplete
    path('suggestionapi/', views.suggestionApi, name="suggestionapi"),

    
    
    






    # change password
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/done_password_change.html'
                                                                            ), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url=reverse_lazy("password_change_done")),
         name='password_change'),


    # Forgot password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_form.html',
         success_url=reverse_lazy("password_reset_complete")), name='password_reset_confirm'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html", success_url=reverse_lazy("password_reset_done"), email_template_name='registration/forgot_password_email.html'),
         name="reset_password"),     # 1
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),    # 2

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/done_password_reset.html"),
         name="password_reset_complete"),   # 4


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
