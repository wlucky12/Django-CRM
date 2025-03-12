import random
import string
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Customer,Account,Transaction
from .forms import SignUpForm,AddRecordForm,TransactionForm
from django.db import IntegrityError,transaction
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from .utils.pagination import Pagination
import json
# Create your views here.
def home(request):
    return render(request,'home.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in')
            return redirect('home')
        else:
            messages.success(request,'There was an error logging in, please try again')
            return redirect('login')
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            # request.session['info'] ={'username':username,'password':password} 
            messages.success(request,'You have successfully registered')
            return redirect('home')
        else:
            messages.success(request,'There was an error registering, please try again')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})

def customer_record(request,pk):

    customer=Customer.objects.get(customer_id=pk)
    return render(request,'record.html',{'customer':customer})

    
def delete_record(request,pk):
        delete_it=Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record deleted successfully')
        return redirect('home')
    
# def luhn_check_digit(number):
#     """ 计算 Luhn 校验位 """
#     digits = list(map(int, str(number)))
#     # 从右向左，偶数位乘以 2（索引从 0 开始，倒数第二位是 -2）
#     for i in range(len(digits) - 2, -1, -2):
#         digits[i] *= 2
#         if digits[i] > 9:
#             digits[i] = digits[i] - 9  # 等价于 (digits[i] // 10) + (digits[i] % 10)
#     total = sum(digits[:-1])  # 排除最后一位（预留的校验位）
#     return str((10 - (total % 10)) % 10)

# def generate_bank_account():
#     """ 生成16位银行卡号 """
#     bank_code = '622848'  # 银行标识
#     middle = ''.join(str(random.randint(0, 9)) for _ in range(9))  # 中间9位
#     base_number = bank_code + middle  # 前15位
#     check_digit = luhn_check_digit(base_number + '0')  # 补位计算校验码
#     return base_number + check_digit
def generate_account_number():
    """ 生成一个随机的 10 位账号 """
    # 使用字母和数字组合
    """ 生成 12 位随机字符串（字母+数字）"""
    characters = string.ascii_letters + string.digits  # 大小写字母 + 数字
    return ''.join(random.choices(characters, k=12))  # 增加长度至 12 位
def add_record(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            max_attempts = 5  # 最大重试次数
            for attempt in range(max_attempts):
                try:
                    with transaction.atomic():
                        customer = form.save()
                        account_number = generate_account_number()
                        Account.objects.create(
                            customer=customer,
                            account_number=account_number,
                            account_type=1,
                            account_balance=10000
                        )
                        messages.success(request, '客户及账户创建成功！')
                        return redirect('home')
                except IntegrityError:
                    if attempt == max_attempts - 1:
                        messages.error(request, '无法生成唯一账号，请稍后重试')
                    continue
                except Exception as e:
                    messages.error(request, f'系统错误：{str(e)}')
                    break
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})
def update_record(request,pk):
    current_record=Customer.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request,'Record updated successfully')
        return redirect('home')
    return render(request,'update_record.html',{'form':form})

def show_data(request):
    # 添加搜索功能
    data_dict = {}
    searched = request.GET.get('q', "")
    if searched:
        data_dict['name__contains'] = searched

    # 获取客户数据
    customers = Customer.objects.filter(**data_dict)

    # 使用分页工具类
    pagination = Pagination(request, customers)
    paginated_customers = pagination.get_paginated_queryset()
    page_info = pagination.get_page_info()

    context = {
        'customers': paginated_customers,
        'searched': searched,
        'page_list': page_info['page_list'],
        'prev_page': page_info['prev_page'],
        'next_page': page_info['next_page'],
    }
    return render(request, 'show_data.html', context)

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
            messages.success(request, '交易创建成功！')
            return redirect('account')
    else:
        form = TransactionForm()
    return render(request, 'transactions.html', {'form': form})

def show_accounts(request):
    # 添加搜索功能
    data_dict = {}
    searched = request.GET.get('q', "")
    if searched:
        data_dict['account_number__contains'] = searched

    # 获取账户数据
    accounts = Account.objects.filter(**data_dict)

    # 使用分页工具类
    pagination = Pagination(request, accounts)
    paginated_accounts = pagination.get_paginated_queryset()
    page_info = pagination.get_page_info()

    # 准备账户数据
    account_list = []
    for account in paginated_accounts:
        account_list.append({
            'account_number': account.account_number,
            'account_type': account.get_account_type_display(),
            'account_balance': account.account_balance,
            'customer_name': account.get_customer_name(),
        })

    context = {
        'accounts': account_list,
        'searched': searched,
        'page_list': page_info['page_list'],
        'prev_page': page_info['prev_page'],
        'next_page': page_info['next_page'],
    }
    return render(request, 'accounts.html', context)

    