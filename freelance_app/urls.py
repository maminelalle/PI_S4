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
    path('client/create-job/', views.client_create_job, name='client_create_job'),
    path('client/jobs/', views.client_job_list, name='client_job_list'),
    path('client/job/<int:pk>/applications/', views.client_view_applications, name='client_view_applications'),
    path('client/messages/', views.client_messages, name='client_messages'),
    path('client/profile/', views.client_profile, name='client_profile'),
    path('client/reviews/', views.client_reviews, name='client_reviews'),
    path('client/resources/', views.client_resources, name='client_resources'),
    path('client/payments/', views.client_payments, name='client_payments'),
    path('client/settings/', views.client_settings, name='client_settings'),
    # # Jobs
    # path('jobs/', views.job_list, name='job_list'),
    # path('jobs/create/', views.job_create, name='job_create'),
    # path('jobs/<int:pk>/edit/', views.job_update, name='job_update'),
    # path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),

    # # Applications
    # path('jobs/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),

    # # Messages
    # path('messages/', views.inbox, name='inbox'),
    # path('messages/send/', views.send_message, name='send_message'),

    # # Resources
    # path('resources/', views.resource_list, name='resource_list'),
    # path('resources/create/', views.resource_create, name='resource_create'),

    # # Reviews
    # path('users/<int:user_id>/review/', views.submit_review, name='submit_review'),

    # # Comments
    # path('resources/<int:resource_id>/comment/', views.comment_create, name='comment_create'),

   
    

]
