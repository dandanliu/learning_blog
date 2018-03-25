"""定义learning_blogs的URL模式"""
from django.urls import path, re_path
from . import views


app_name='learning_blogs'

urlpatterns = [
    #主页
    path('index/', views.index, name='index'),

    #显示所有标题
    re_path(r'^topics/$', views.topics, name='topics'),

    # 特定主题的详细页面
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # 用于添加新主题的网页
    re_path(r'^new_topic/$', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # 用于编辑条目的页面
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

]
