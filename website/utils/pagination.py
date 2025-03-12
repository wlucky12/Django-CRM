from django.utils.safestring import mark_safe

class Pagination:
    """
    分页工具类，用于处理分页逻辑。

    使用方法：
    1. 初始化时传入 request 和 queryset：
       pagination = Pagination(request, queryset, page_size=10)
    2. 获取分页后的数据：
       paginated_data = pagination.get_paginated_queryset()
    3. 获取分页信息（上一页、下一页、分页链接）：
       page_info = pagination.get_page_info()
    4. 在模板中使用 page_info 渲染分页导航：
       {{ page_info.page_list|safe }}
    """

    def __init__(self, request, queryset, page_size=10):
        """
        初始化分页工具类。

        参数：
        - request: Django 的 request 对象，用于获取当前页码
        - queryset: 需要分页的查询集
        - page_size: 每页显示的数据量，默认为 10
        """
        self.request = request
        self.queryset = queryset
        self.page_size = page_size
        self.page = int(request.GET.get('page', 1))  # 获取当前页码，默认为 1
        self.start = (self.page - 1) * self.page_size  # 计算起始位置
        self.end = self.page * self.page_size  # 计算结束位置

    def get_paginated_queryset(self):
        """
        获取分页后的查询集。

        返回：
        - 分页后的查询集
        """
        return self.queryset[self.start:self.end]

    def get_page_info(self):
        """
        获取分页信息，包括上一页、下一页和分页链接。

        返回：
        - 包含分页信息的字典：
          {
              'prev_page': 上一页页码,
              'next_page': 下一页页码,
              'page_list': 分页链接的 HTML 字符串
          }
        """
        total_items = self.queryset.count()  # 获取总数据量
        total_pages = total_items // self.page_size  # 计算总页数
        if total_items % self.page_size != 0:
            total_pages += 1

        # 计算上一页和下一页
        prev_page = max(1, self.page - 1)
        next_page = min(total_pages, self.page + 1)

        # 生成分页链接
        page_list = []
        for i in range(1, total_pages + 1):
            page_list.append(f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>')
        page_list = mark_safe(''.join(page_list))  # 标记为安全字符串

        return {
            'prev_page': prev_page,
            'next_page': next_page,
            'page_list': page_list,
        } 