import datetime
from _md5 import md5

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator

from JiewuOnline.settings import MEDIA_URL
from apps.courses.models import Course, CourseTag, CourseResource, Video, AgeLay, CourseStudent
from apps.operations.models import UserFavorite, UserCourse, CourseComments, UserOrder, UserMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class CourseBuyView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        buy_course = Course.objects.get(id=int(course_id))
        userorder = UserOrder.objects.create(course=buy_course, user=request.user, status=1, price=buy_course.price)
        host = request.get_host()
        return render(request, "course-buy.html",{
        "buy_course":buy_course,
        "userorder":userorder,
        "host":host,
           })

    def post(self, request, *args, **kwargs):
        goodsname = request.POST.get("goodsname")
        istype = request.POST.get("istype")
        notify_url = request.POST.get("notify_url")
        orderid = request.POST.get("orderid")
        orderuid = str(request.user.id)
        price = request.POST.get("price")
        return_url = request.POST.get("return_url")
        token = 'f19a2b4b5dc2f41d51c40342c902fdd8'
        uid = '54212bb69c633f47717975b5'
        key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode("utf-8")).hexdigest()
        UserOrder.objects.filter(id=int(orderid)).update(istype=int(istype))
        return JsonResponse({
                 "status" : 'success',
                 "key": key,
           })


class VideoView(LoginRequiredMixin, View):
    #login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources":course_resources,
            "MEDIA_URL": MEDIA_URL,
            "related_courses":related_courses,
            "video":video,
        })


class CourseCommentsView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        #查询用户是否已经关联该课程
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)


        return render(request,"course-comment.html",{
            "course":course,
            "MEDIA_URL": MEDIA_URL,
            "course_resources":course_resources,
            "related_courses":related_courses,
            "comments":comments,
        })

class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        #1. 用户和课程之间的关联
        #2. 对view进行login登录的验证
        #3. 其他课程

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources":course_resources,
            "related_courses":related_courses
        })

class CourseDetailView(View):
    """
    获取课程详情
    """
    def get(self, request, course_id, *args, **kwargs):
        orderid = request.GET.get('orderid')
        if orderid:
            UserOrder.objects.filter(id=int(orderid)).update(status=2)
             # 查询用户是否已经关联了该课程
            course = Course.objects.get(id=int(course_id))
            CourseStudent.objects.create(user=request.user, course=course,teacher_name=course.teacher.name)
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
                course.students += 1
                course.save()

            course.click_nums += 1
            course.save()

            # 获取收藏状态
            has_fav_course = False
            has_fav_org = False

            # 判断用户是否登录
            if request.user.is_authenticated:
                if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                    has_fav_course = True
                if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                    has_fav_org = True

            # 获取购买状态
            has_bug_course = False
            if request.user.is_authenticated:
                user_bug_course = UserCourse.objects.filter(user=request.user, course=course)
                if user_bug_course:
                    has_bug_course = True

            #获取预约状态
            has_apo_course = False
            is_apo_course = CourseStudent.objects.filter(course_id=course_id, user_id=request.user.id,is_apoints=True)
            if is_apo_course:
                has_apo_course = True


            # 获取是否还可以预约
            has_op_course = False
            # 课程开始前3个小时还可以预约
            if course.start_time >= datetime.datetime.now() + datetime.timedelta(hours=3):
                has_op_course = True
            else:
                mecourse = Course.objects.get(id=int(course_id))
                tip_message = "离上课时间小于3个小时，已经不能预约课程！"
                usermessage = UserMessage()
                usermessage.user = request.user
                usermessage.message = tip_message
                usermessage.save()

            # 获取是否还可以取消预约
            has_is_capo_course = False
            if is_apo_course:
                is_course = Course.objects.get(id=int(course_id))
                # 课程开始前3个小时还可以取消预约
                if is_course.start_time <= datetime.datetime.now() + datetime.timedelta(hours=3):
                    # 剩余时间小于三个小时不能取消
                    has_is_capo_course = True
                    mecourse = Course.objects.get(id=int(course_id))
                    tip_message = "你预约的" + mecourse.name + "课程，离上课时间小于3个小时，已经不能取消预约！"
                    usermessage = UserMessage()
                    usermessage.user = request.user
                    usermessage.message = tip_message
                    usermessage.save()

            # 通过课程的tag做课程的推荐
            """
            tag = course.tag
            related_courses = []
            if tag:
                #排除掉当前的课程
                related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]
            """

            tags = course.coursetag_set.all()
            tag_list = [tag.tag for tag in tags]

            course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)[:3]
            related_courses = []
            for course_tag in course_tags:
                related_courses.append(course_tag.course)

            return render(request, "course-detail.html", {
                "course": course,
                "MEDIA_URL": MEDIA_URL,
                "has_fav_course": has_fav_course,
                "has_fav_org": has_fav_org,
                "related_courses": related_courses,
                "has_bug_course": has_bug_course,
                "has_apo_course":has_apo_course,
                "has_is_capo_course": has_is_capo_course,
                "has_op_course": has_op_course,
            })

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

         #获取收藏状态
        has_fav_course = False
        has_fav_org = False

        #判断用户是否登录
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 获取购买状态
        has_bug_course = False
        if request.user.is_authenticated:
            user_bug_course= UserOrder.objects.filter(user=request.user, course=course,status=2)
            if user_bug_course:
                has_bug_course = True

        # 获取预约状态
        has_apo_course = False
        is_apo_course = CourseStudent.objects.filter(course_id=course_id, user_id=request.user.id,is_apoints=True)
        if is_apo_course:
            has_apo_course = True

        # 获取是否还可以预约
        has_op_course = False
        # 课程开始前3个小时还可以预约
        if course.start_time >= datetime.datetime.now() + datetime.timedelta(hours=3):
            has_op_course = True
        else:
            mecourse = Course.objects.get(id=int(course_id))
            tip_message = "离上课时间小于3个小时，已经不能预约课程！"


        # 获取是否还可以取消预约
        has_is_capo_course = False
        if is_apo_course:
            is_course = Course.objects.get(id=int(course_id))
            # 课程开始前3个小时还可以取消预约
            if is_course.start_time <= datetime.datetime.now() + datetime.timedelta(hours=3):
                # 剩余时间小于三个小时不能取消
                has_is_capo_course = True
                mecourse = Course.objects.get(id=int(course_id))
                tip_message = "你预约的" + mecourse.name + "课程，离上课时间小于3个小时，已经不能取消预约！"
                usermessage = UserMessage()
                usermessage.user = request.user
                usermessage.message = tip_message
                usermessage.save()

            # 课程开始前3个小时还可以取消预约
            if is_course.start_time <= datetime.datetime.now() + datetime.timedelta(hours=3):
                #剩余时间小于三个小时不能取消
                has_is_capo_course = True
                mecourse = Course.objects.get(id=int(course_id))
                tip_message = "你预约的" + mecourse.name + "课程，离开课时间小于3个小时，已经不能取消预约！"
                usermessage = UserMessage()
                usermessage.user = request.user
                usermessage.message = tip_message
                usermessage.save()

        # 通过课程的tag做课程的推
        """
        tag = course.tag
        related_courses = []
        if tag:
            #排除掉当前的课程
            related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]
        """

        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)[:3]
        related_courses = []
        for course_tag in course_tags:
            related_courses.append(course_tag.course)

        return render(request,"course-detail.html",{
            "course":course,
            "MEDIA_URL": MEDIA_URL,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
            "has_bug_course":has_bug_course,
            "has_apo_course": has_apo_course,
            "has_is_capo_course":has_is_capo_course,
             "has_op_course":has_op_course,
        })

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        user_id = request.POST.get("user_id")
        # 是否已经预约
        existed_apoints = CourseStudent.objects.filter(course_id=int(course_id),user_id=int(user_id),is_apoints=True)
        if existed_apoints:
            existed_apoints.update(is_apoints=False)
            course = Course.objects.get(id=int(course_id))
            tip_message = "你已经取消了"+course.name+"课程的预约！"
            usermessage = UserMessage()
            usermessage.user = request.user
            usermessage.message =tip_message
            usermessage.save()
            return JsonResponse({
                 "status" : 'success',
                 "msg": "预约",
                 "tip_message": tip_message,
             })
        else:
            CourseStudent.objects.filter(course_id=course_id, user_id=user_id).update(is_apoints=True)
            course = Course.objects.get(id=int(course_id))
            tip_message = "你已经预约了"+course.name+"课程，该课程在"+str(course.start_time)+"开始上课，请你按时到该课所在的机构的地址上课！（开课前的3个小时可以取消预约）"
            usermessage = UserMessage()
            usermessage.user = request.user
            usermessage.message = tip_message
            usermessage.save()
            return JsonResponse({
                "status": 'success',
                "msg": "已预约",
                "tip_message":tip_message,
            })

class CourseListView(View):
    # 获取课程信息
    def get(self, request,  *args, **kwargs):
        course_num = Course.objects.all().count()
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]
        all_ages = AgeLay.objects.all()
        #搜索关键词
        keyworks = request.GET.get("keywords","")
        s_type = "course"
        if keyworks:
            all_courses = all_courses.filter(Q(name__icontains=keyworks)|Q(desc__icontains=keyworks)|Q(detail__icontains=keyworks))

        # 对课程难度进行筛选
        degree = request.GET.get("de", "")
        if degree:
            all_courses = all_courses.filter(degree=degree)

        # 对舞的种类进行筛选
        category = request.GET.get("cg", "")
        if category:
            all_courses = all_courses.filter(category=category)

        # 通过年龄段对课程机构进行筛选
        age_id = request.GET.get("age", "")
        if age_id:
            if age_id.isdigit():
                all_courses = all_courses.filter(age_id=int(age_id))

        #对课程排序
        sort = request.GET.get("sort","")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 对课程数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=6, request=request)
        courses = p.page(page)
        return render(request,"course-list.html",{
            "all_courses":courses,
            "MEDIA_URL":MEDIA_URL,
            "sort":sort,
            "hot_courses":hot_courses,
            "keyworks":keyworks,
            "s_type":s_type,
            "all_ages":all_ages,
            "degree": degree,
            "age_id": age_id,
            "category":category,
            "course_num":course_num,
        })