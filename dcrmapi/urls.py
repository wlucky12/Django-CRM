from rest_framework.routers import DefaultRouter
from .views import apiviews



router = DefaultRouter()
router.register('customers', apiviews.CustomerViewSet)
router.register('accounts', apiviews.AccountViewSet)
router.register('transactions', apiviews.TransactionViewSet)
router.register('analysis', apiviews.AnalysisViewSet, basename='analysis')  # 注册 AnalysisViewSet

urlpatterns = router.urls