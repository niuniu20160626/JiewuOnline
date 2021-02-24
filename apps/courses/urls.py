from django.conf.urls import url
from django.urls import path

from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView, VideoView,CourseBuyView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    url(r'^(?P<course_id>\d+)/buy/$', CourseBuyView.as_view(), name="buy"),
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),
]