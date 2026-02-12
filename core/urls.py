from django.urls import path
from .views import *


urlpatterns = [
    path('', login_view, name='login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('owner-dashboard/', owner_dashboard, name='owner_dashboard'),
    path('create-owner/', create_owner, name='create_owner'),
    path('create-tenant/',create_tenant,name='create_tenant'),
    path('create-bill',create_bill,name='create_bill'),
    path('tenant-dashboard/',tenant_dashboard,name='tenant_dashboard'),
    path('logout',logout_view,name='logout'),
    path('view-bills',owner_bills,name='view_bills'),



]

