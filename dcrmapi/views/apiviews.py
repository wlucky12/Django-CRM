from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from website.models import Customer, Account, Transaction  # 从 website 应用中导入模型
from ..sers import CustomerSerializer, AccountSerializer, TransactionSerializer
from rest_framework.pagination import PageNumberPagination
from django.db import transaction,IntegrityError,models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import random

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5  # 每页显示5条数据
    page_size_query_param = 'page_size'
    max_page_size = 100
def generate_account_number():
    """ 生成一个随机的 12 位账号 """
    characters = string.ascii_letters + string.digits  # 大小写字母 + 数字
    return ''.join(random.choices(characters, k=12))  # 生成 12 位随机字符串
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """
        创建客户时自动为其生成一个默认账户
        """
        max_attempts = 5  # 最大重试次数
        for attempt in range(max_attempts):
            try:
                with transaction.atomic():
                    customer = serializer.save()  # 保存客户
                    account_number = generate_account_number()  # 生成随机账号
                    Account.objects.create(
                        customer=customer,
                        account_number=account_number,
                        account_type=1,  # 默认账户类型为活期
                        account_balance=10000  # 默认余额为10000元
                    )
                    break  # 成功创建后退出循环
            except IntegrityError:
                if attempt == max_attempts - 1:
                    raise IntegrityError("无法生成唯一账号，请稍后重试")
                continue  # 如果账号重复，重试
            except Exception as e:
                raise Exception(f"系统错误：{str(e)}")

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)  # 使用 'search' 作为搜索参数
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)  # 使用 icontains 进行模糊匹配
        return queryset

class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Account.objects.all()
        customer_id = self.request.query_params.get('customer_id', None)  # 通过 customer_id 查询
        search_query = self.request.query_params.get('search', None)  # 通过 search 参数搜索

        if customer_id:
            queryset = queryset.filter(customer__customer_id=customer_id)  # 根据 customer_id 过滤

        if search_query:
            queryset = queryset.filter(
                models.Q(account_number__icontains=search_query) |  # 根据账户号搜索
                models.Q(customer__name__icontains=search_query)  # 根据客户名字搜索
            )

        return queryset

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination  # 添加分页功能
    from django.db.models import Q  # 导入 Q 对象

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)  # 获取搜索参数

        if search_query:
            queryset = queryset.filter(
                models.Q(account__customer__name__icontains=search_query) |  # 根据账户客户姓名搜索
                models.Q(target_account__customer__name__icontains=search_query)  # 根据目标账户客户姓名搜索
            )

        return queryset

class AnalysisViewSet(ViewSet):
    @method_decorator(csrf_exempt)
    @method_decorator(xframe_options_exempt)
    def list(self, request):
        # 账户类型分布
        account_type_data = Account.objects.values('account_type').annotate(count=Count('id'))
        account_type_list = [{'value': item['count'], 'name': '活期' if item['account_type'] == 1 else '定期'} 
                            for item in account_type_data]
        
        # 交易类型分布
        transaction_type_data = Transaction.objects.values('transaction_type').annotate(count=Count('id'))
        transaction_type_list = [{'value': item['count'], 'name': item['transaction_type']} 
                                for item in transaction_type_data]
        
        # 每日交易金额趋势
        daily_transactions = Transaction.objects.annotate(
            transaction_date=TruncDate('date')
        ).values('transaction_date').annotate(
            total_amount=Sum('amount')
        ).order_by('transaction_date')
        
        dates = []
        amounts = []
        for item in daily_transactions:
            dates.append(item['transaction_date'].strftime('%Y-%m-%d'))
            amounts.append(float(item['total_amount']))  # 将 Decimal 转换为 float
        
        response_data = {
            'account_type_data': account_type_list,
            'transaction_type_data': transaction_type_list,
            'transaction_dates': dates,
            'transaction_amounts': amounts,
        }
        
        return Response(response_data)