# process的二级目录设置
from django.conf.urls import url
from app.process import process_views


urlpatterns = [
    # 人员-添加
    # url(r'^person_add', views.Processor_Add),
    # 人员-查询
    url(r'^processor_inquiry/$', process_views.Processor_Inquiry),
    # 人员-更改
    url(r'^processor_update/$',process_views.Processor_Update),
    # 人员-删除
    # url(r'^processor_delete/$',views.Processor_Delete),

    # 结果-提交
    url(r'^processtion_add',process_views.ProcessData_Add),
    # 结果-查询
    url(r'^processtion_inquiry/$',process_views.ProcessData_Inquiry),  # 一对多

]

