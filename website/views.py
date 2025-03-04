import random
import string
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Customer,Account,Transaction
from .forms import SignUpForm,AddRecordForm
from django.db import IntegrityError,transaction
from django.utils.safestring import mark_safe
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
    return render(request,'login.html',{})

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
            messages.success(request,'You have successfully registered')
            return redirect('home')
        else:
            messages.success(request,'There was an error registering, please try again')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer=Customer.objects.get(customer_id=pk)
        return render(request,'record.html',{'customer':customer})
    else:
        messages.success(request,'You must be logged in to view that page')
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request,'You must be logged in to view that page')
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
    if not request.user.is_authenticated:
        return redirect('login')
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
    if request.user.is_authenticated:
        current_record=Customer.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record updated successfully')
            return redirect('home')
        return render(request,'update_record.html',{'form':form})

def show_data(request): 
    #添加搜索功能
    data_dict={}
    searched = request.GET.get('q',"")
    if searched:
        data_dict['name__contains'] = searched

    #添加分页功能  
    page= int(request.GET.get('page',1))
    
    
    start=(page-1)* 10
    end=page * 10
    customers=Customer.objects.filter(**data_dict)[start:end]

    #获取数据量并生成页面数量返回前端
    pages=Customer.objects.filter(**data_dict).count()
    if pages % 10 == 0:
        pages = pages // 10
    else:
        pages = pages // 10 + 1
    
    #上一页
    priv=max(1,page-1)
    #下一页
    next=min(pages,page+1)
    page_list=[]
    for i in range(1,pages+1):
        ele ='<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i,i)
        page_list.append(ele)
    #将列表转换成字符串,并标记为安全
    #问题：当数据过多时页面太多，前端展示效果不佳
    page_list = mark_safe(''.join(page_list) )


    #改进：能否通过异步请求拿到数据
    return render(request,'show_data.html',{'customers':customers,'searched':searched,'page_list':page_list,'priv':priv,'next':next})



def transactions(request):
    pass