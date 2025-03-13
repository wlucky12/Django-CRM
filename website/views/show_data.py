from ..models import Customer
from ..utils.pagination import Pagination
from django.shortcuts import render


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