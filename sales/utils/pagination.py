'''
自定义分页组件
'''
import copy

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_parm="page", plus=5):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get('page', '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_parm = page_parm
        self.queryset = queryset[self.start:self.end]
        self.totle_count = queryset.count()
        totle_page_count, div = divmod(self.totle_count, page_size)
        if div:
            totle_page_count = totle_page_count + 1
        self.totle_page_count = totle_page_count
        self.plus = plus

    def html(self):
        if self.totle_page_count < 2 * self.plus:
            before_page = 1
            after_page = self.totle_page_count
        else:
            if self.page <= self.plus:
                before_page = 1
                after_page = 2 * self.plus
            else:
                if (self.page + self.plus) > self.totle_page_count:
                    before_page = self.totle_page_count - 2 * self.plus
                    after_page = self.totle_page_count
                else:
                    before_page = self.page - self.plus
                    after_page = self.page + self.plus
            # 首页
        li_strlist = []  # 存放要插到ul标签里面的li标签
        self.query_dict.setlist(self.page_parm, [1])

        prev_page = '<li class="page-item "><a class="page-link" href="?{}">首页</a></li>'.format(
            self.query_dict.urlencode())
        li_strlist.append(prev_page)
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_parm, [self.page - 1])
            prev_page = '<li class="page-item "><a class="page-link" href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())
            li_strlist.append(prev_page)
        else:
            self.query_dict.setlist(self.page_parm, [1])
            prev_page = '<li class="page-item "><a class="page-link" href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode()
            )
            li_strlist.append(prev_page)

        for i in range(before_page, after_page + 1):
            self.query_dict.setlist(self.page_parm, [i])

            if self.page == i:
                li_str = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                li_str = '<li class="page-item "><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            li_strlist.append(li_str)

        # 下一页
        if self.page < self.totle_page_count:
            self.query_dict.setlist(self.page_parm, [self.page + 1])
            prev_page = '<li class="page-item "><a class="page-link" href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
            li_strlist.append(prev_page)
        else:
            self.query_dict.setlist(self.page_parm, [self.totle_page_count])
            prev_page = '<li class="page-item "><a class="page-link" href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
            li_strlist.append(prev_page)
        # 尾页
        self.query_dict.setlist(self.page_parm, [self.totle_page_count])
        prev_page = '<li class="page-item "><a class="page-link" href="?{}">尾页</a></li>'.format(
            self.query_dict.urlencode())
        li_strlist.append(prev_page)
        page_string = mark_safe("".join(li_strlist))
        return page_string
