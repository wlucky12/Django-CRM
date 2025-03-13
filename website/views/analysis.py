from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from ..models import Account, Transaction
import json

def analysis(request):
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
    
    context = {
        'account_type_data': json.dumps(account_type_list),
        'transaction_type_data': json.dumps(transaction_type_list),
        'transaction_dates': json.dumps(dates),
        'transaction_amounts': json.dumps(amounts),
    }
    return render(request, 'analysis.html', context) 