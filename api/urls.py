from django.urls import path
from . import views
urlpatterns = [

    path('customer-regist/', views.CustomerRegist.as_view(), name="customer-regist"),
    path('create-otp/', views.createOtp, name="create-otp"),
    path('accept-otp/', views.acceptOtp, name="accept-otp"),
    path('create-password/', views.createPassword, name="create-password"),
    path('get-customer-user/', views.getCustomerUser, name="get-customer-user"),

]
