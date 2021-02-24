from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, \
    TeacherListView, TeacherDetailView, OrgInfoView, OrgJchfView, OrgCourseCardView, OrgJchfPlayView, NoticDetailView, \
    OrgCourseCardDetailView, OrgCourseCardBuyView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),

    #讲师相关界面
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

    #关于我们界面
    url(r'^orginfo/$', OrgInfoView.as_view(), name="orginfo"),

    #精彩回放界面
    url(r'^orgjchf/$', OrgJchfView.as_view(), name="orgjchf"),
    url(r'^orgjchf/(?P<jchf_id>\d+)/$', OrgJchfPlayView.as_view(), name="orgjchfplay"),

    #课程售卖界面
    url(r'^coursecard/$', OrgCourseCardView.as_view(), name="coursecard"),
    url(r'^coursecard/(?P<coursecard_id>\d+)$', OrgCourseCardDetailView.as_view(), name="c_desc"),
    url(r'^buycoursecard/(?P<coursecard_id>\d+)$', OrgCourseCardBuyView.as_view(), name="buy_card"),

    url(r'^notic/(?P<notic_id>\d+)/$', NoticDetailView.as_view(), name="notic"),
]
