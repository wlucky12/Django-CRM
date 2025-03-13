from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Account
from django.utils.safestring import mark_safe

def show_accounts(request):
    # 添加搜索功能
    data_dict = {}
    searched = request.GET.get('q', "")
    if searched:
        data_dict['account_number__contains'] = searched

    # 添加分页功能
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每页显示10条数据
    start = (page - 1) * page_size
    end = page * page_size

    # 获取账户数据
    accounts = Account.objects.filter(**data_dict)[start:end]

    # 计算总页数
    total_accounts = Account.objects.filter(**data_dict).count()
    total_pages = total_accounts // page_size
    if total_accounts % page_size != 0:
        total_pages += 1

    # 上一页和下一页
    prev_page = max(1, page - 1)
    next_page = min(total_pages, page + 1)

    # 生成分页链接
    page_list = []
    for i in range(1, total_pages + 1):
        page_list.append(f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>')
    page_list = mark_safe(''.join(page_list))

    # 准备账户数据
    account_list = []
    for account in accounts:
        account_list.append({
            'account_number': account.account_number,
            'account_type': account.get_account_type_display(),
            'account_balance': account.account_balance,
            'customer_name': account.get_customer_name(),
        })

    context = {
        'accounts': account_list,
        'searched': searched,
        'page_list': page_list,
        'prev_page': prev_page,
        'next_page': next_page,
    }
    return render(request, 'accounts.html', context) 