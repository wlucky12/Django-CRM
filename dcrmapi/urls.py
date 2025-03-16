from rest_framework.routers import DefaultRouter
from .views import apiviews,authapi
from django.urls import path


router = DefaultRouter()
router.register('customers', apiviews.CustomerViewSet)
router.register('accounts', apiviews.AccountViewSet)
router.register('transactions', apiviews.TransactionViewSet)
router.register('analysis', apiviews.AnalysisViewSet, basename='analysis')  # 注册 AnalysisViewSet




urlpatterns = [
    path('set-csrf-token/', authapi.set_csrf_token, name='set-csrf-token'),
    path('login/', authapi.login_view, name='login'),
    path('logout/', authapi.logout_view, name='logout'),
    path('user/', authapi.user, name='user'),
    path('register/', authapi.register, name='register'),
]
urlpatterns += router.urls
