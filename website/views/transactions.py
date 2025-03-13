from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import TransactionForm
from ..models import Transaction, Account

def transactions(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            account = transaction.account
            target_account = transaction.target_account
            amount = transaction.amount

            if transaction.transaction_type == 'deposit':
                account.account_balance += amount
            elif transaction.transaction_type == 'withdrawal':
                account.account_balance -= amount
            elif transaction.transaction_type == 'transfer':
                account.account_balance -= amount
                target_account.account_balance += amount
                target_account.save()

            account.save()
            transaction.save()
            return redirect('transaction_list')  # 假设你有一个交易列表页面
    else:
        form = TransactionForm()
    return render(request, 'website/transaction_form.html', {'form': form}) 

from django.http import JsonResponse
from ..models import Account

def check_account_type(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        return JsonResponse({
            'account_type': account.account_type,
        })
    except Account.DoesNotExist:
        return JsonResponse({
            'error': '账户不存在',
        }, status=404)

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')  # 按日期降序排列
    context = {
        'transactions': transactions,
    }
    return render(request, 'website/transaction_list.html', context)