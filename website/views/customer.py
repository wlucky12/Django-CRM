from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import LoginForm,AddRecordForm
from ..models import Customer,Account
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError,transaction
import random
import string

# def login_customer(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             phone_number = form.cleaned_data['phone_number']
#             password = form.cleaned_data['password']
#             try:
#                 customer = Customer.objects.get(phone_number=phone_number)
#                 if customer and customer.check_password(password):  # 确保 customer 不是 None
#                     # 登录成功，跳转到 customer_page 视图
#                     return redirect('home')
#                 else:
#                     messages.error(request, '密码错误。')
#             except Customer.DoesNotExist:
#                 messages.error(request, '手机号不存在。')
#     else:
#         form = LoginForm()
#     return render(request, 'website/customer_login.html', {'form': form}) 

def forgot_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, '密码不匹配。')
            return redirect('forgot_password')

        try:
            customer = Customer.objects.get(phone_number=phone_number)
            customer.password = make_password(new_password)  # 哈希存储新密码
            customer.save()
            messages.success(request, '密码已成功更新。')
            return redirect('login')
        except Customer.DoesNotExist:
            messages.error(request, '手机号不存在。')
            return redirect('forgot_password')
    return render(request, 'website/forgot_password.html')

def customer_page(request):
    return render(request, 'website/customer_page.html')

def customer_record(request,pk):
    customer=Customer.objects.get(customer_id=pk)
    return render(request,'record.html',{'customer':customer})
def delete_record(request,pk):
        # delete_it=Customer.objects.get(customer_id=pk)
        # delete_it.delete()
        messages.success(request,'Record deleted successfully，为了数据稳定性，暂时无法删除，因为信息联系到账户')
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
    current_record=Customer.objects.get(customer_id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request,'Record updated successfully')
        return redirect('home')
    return render(request,'update_record.html',{'form':form})