from django.utils.safestring import mark_safe


class MyPagenation(): #创建类 进行分页的逻辑封装

    def __init__(self,page_num,total_count,per_page_num,page_num_show,base_url):#我们所需参数

        self.per_page_num = per_page_num  # 每页显示10条
        # 页面生成页码的数量
        self.page_num_show = page_num_show  # 7      4 5 6 7 8
        self.base_url = base_url  # 7      4 5 6 7 8
        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1
        self.page_num = page_num

        shang, yu = divmod(total_count, self.per_page_num)  # shang:商    yu：余数
        # 总页码数展示
        if yu:
            page_num_count = shang + 1
        else:
            page_num_count = shang
        self.page_num_count = page_num_count
        # 对当前页码进行判断...避免搞事情发生
        if page_num <= 0:
            page_num = 1
        elif page_num > page_num_count:
            page_num = page_num_count

        # 3 4 5 6 7    4 5 6 7 8 9 10
        #让其显示我们所要的页码数
        half_show = self.page_num_show // 2  # 2
        # 不能让其有0 和负的页码数
        if page_num - half_show <= 0:
            start_page_num = 1
            end_page_num = self.page_num_show + 1  # 9

        # 不能让其页码数超过实际有的页码数
        elif page_num + half_show > page_num_count:
            start_page_num = page_num_count - self.page_num_show + 1  # 26 - 5 = 21
            end_page_num = page_num_count + 1  # 27  [21,22,23,24,25,26]
        else:
            start_page_num = page_num - half_show  # 4  1
            end_page_num = page_num + half_show + 1  # 9  6

        self.start_page_num = start_page_num
        self.end_page_num = end_page_num
    # 给起始 和终止页码显示变化封装 属性
    @property
    def start_data_num(self):
        return (self.page_num - 1) * self.per_page_num

    @property
    def end_data_num(self):
        return self.page_num * self.per_page_num

    def page_hmtl(self):
        page_num_range = range(self.start_page_num, self.end_page_num)
        page_html = ''
        page_pre_html = '<nav aria-label="Page navigation"><ul class="pagination">'
        page_html += page_pre_html
        #首页
        first_page_html = '<li><a href="{1}?page={0}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(1, self.base_url)
        page_html += first_page_html
        # 往前翻页
        if self.page_num <= 1:
            pre_page = '<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.page_num - 1)
        else:
            pre_page = '<li><a href="{1}?page={0}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.page_num - 1,self.base_url)

        page_html += pre_page
        # 对每一页有点击选中样式
        for i in page_num_range:
            if i == self.page_num:
                page_html += '<li class="active"><a href="{1}?page={0}">{0}</a></li>'.format(i,self.base_url)
            else:
                page_html += '<li><a href="{1}?page={0}">{0}</a></li>'.format(i,self.base_url)
        # 往后翻页
        if self.page_num >= self.page_num_count:
            page_next_html = '<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                self.page_num + 1)
        else:
            page_next_html = '<li><a href="{1}?page={0}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                self.page_num + 1,self.base_url)
        page_html += page_next_html
        #尾页
        last_page_html = '<li><a href="{1}?page={0}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'.format(
            self.page_num_count, self.base_url)
        page_html += last_page_html
        end_html = '</ul></nav>'
        page_html += end_html

        return mark_safe(page_html)