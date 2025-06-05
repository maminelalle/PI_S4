from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'), 
    
    #registrer et login
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Pages client
    path('dashboard_client/', views.client_dashboard, name='dashboard_client'),
    # path('client/create-job/', views.client_create_job, name='client_create_job'),
    # path('client/jobs/', views.client_job_list, name='client_job_list'),
    path('client/create-job/', views.client_create_job, name='client_create_job'),
    path('client/jobs/', views.client_job_list, name='client_job_list'),
    path('client/messages/', views.client_messages, name='client_messages'),
    path('client/get-messages/', views.get_messages, name='get_messages'),
    # <int:pk>/
    path('client/job/applications/', views.client_view_applications, name='client_view_applications'),
    # path('client/messages/', views.client_messages, name='client_messages'),
    path('client/profile/', views.client_profile, name='client_profile'),
    path('client/reviews/', views.client_reviews, name='client_reviews'),
    path('client/resources/', views.client_resources, name='client_resources'),
    path('client/payments/', views.client_payments, name='client_payments'),
    path('client/settings/', views.client_settings, name='client_settings'),
     


]
