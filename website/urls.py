from django.urls import path
from .views import views
from .views.show_data import show_data
from .views.accounts import show_accounts
from .views.transactions import transactions,check_account_type, transaction_list
from .views.analysis import analysis
from rest_framework.routers import DefaultRouter
from .views import apiviews

# router = DefaultRouter()
# router.register('customers', apiviews.CustomerViewSet)
# router.register('accounts', apiviews.AccountViewSet)
# router.register('transactions', apiviews.TransactionViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_user, name='login'),                     
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='customer_record'),
    path('delete/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update/<int:pk>', views.update_record, name='update_record'),
    path('show_data/',show_data,name='show_data'),
    path('analysis/', analysis, name='analysis'),
    path('transactions',transactions,name='transactions'),
    path('accounts/', show_accounts, name='show_accounts'),
    path('check_account_type/<int:account_id>/', check_account_type, name='check_account_type'),
    path('transactions/list', transaction_list, name='transaction_list'),
    # path('add_message/<str:message>/<str:level>/', views.add_message, name='add_message'),
]