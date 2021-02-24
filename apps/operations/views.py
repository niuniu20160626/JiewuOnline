from django.core.paginator import PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator

from apps.operations.forms import UserFavForm, CommentsForm
from apps.operations.models import UserFavorite, CourseComments
from django.http import JsonResponse
from apps.courses.models import Course
from apps.courses.models import CourseOrg
from apps.organizations.models import Teacher, Notic
from apps.operations.models import Banner

class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        all_notics = Notic.objects.all()

        # 对精彩回放数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_notics, per_page=8, request=request)
        notics = p.page(page)

        return render(request, "index.html",{
            "banners":banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "notics":notics,
        })

class CommentView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"用户未登录"
            })

        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })



class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        #先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"用户未登录"
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]
            #是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                #用户以后收藏过了,把用户收藏表的记录去掉
                existed_records.delete()

                if fav_type == 1:#取消课程的收藏
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:#取消课程机构的收藏
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:#取消老师的收藏
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                #用户还没有收藏，在用户收藏表中添加收藏记录
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                # 每个收藏类中增加 fav_nums
                if fav_type == 1:#课程的收藏
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:#课程机构的收藏
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == 3:#老师的收藏
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })
