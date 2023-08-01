from django.urls import path
from. import views


app_name = 'core'

urlpatterns = [

    path("", views.Index.as_view(), name="index"),
    path("contactusclass", views.ContactUs.as_view(), name="contactusclass"),
    path("contactus", views.Contactus, name="contactus"),
    path("contactus2", views.contactus2, name="contactus2"),
    
     # Authentication Endpoints
    path('signup/', views.RegisterView.as_view(), name="signup"),
    # path('signupseller/', views.RegisterViewSeller.as_view(), name="signupseller"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
   


     
    
]
