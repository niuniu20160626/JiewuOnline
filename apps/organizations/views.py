from _md5 import md5
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from JiewuOnline.settings import MEDIA_URL
from apps.courses.models import Course
from apps.operations.models import UserFavorite, JchfComments, UserCardOrder, UserCourseCard
from apps.organizations.models import CourseOrg, Teacher, Jchf, Notic, CourseCard
from apps.organizations.models import City
from apps.organizations.forms import AddAskForm, JchfCommentsForm
from django.http import JsonResponse

# Create your views here

class OrgCourseCardBuyView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request,coursecard_id, *args, **kwargs):
        coursecard = CourseCard.objects.get(id=int(coursecard_id))
        usercardorder = UserCardOrder.objects.create(coursecard=coursecard, user=request.user, status=1, price=coursecard.price)
        host = request.get_host()
        return render(request, "org-coursecard-buy.html",{
            "coursecard":coursecard,
            "usercardorder": usercardorder,
            "host": host,
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
        UserCardOrder.objects.filter(id=int(orderid)).update(istype=int(istype))
        return JsonResponse({
                 "status" : 'success',
                 "key": key,
           })

class OrgCourseCardDetailView(View):
    def get(self, request,coursecard_id, *args, **kwargs):

        orderid = request.GET.get('orderid')
        if orderid:
            UserCardOrder.objects.filter(id=int(orderid)).update(status=2)
            coursec = CourseCard.objects.get(id=int(coursecard_id))

            user_course = UserCourseCard(user=request.user,coursecard=coursec,has_time=datetime.datetime.now())
            user_course.save()

            if coursec.card_type == 'ck':
                if coursec.nums == 1:
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(days=1))
                else:
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(years=1))

            if coursec.card_type == 'tk':
                if coursec.name == '周通卡':
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(days=7))
                if coursec.name == '月通卡':
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(days=30))
                if coursec.name == '半年卡':
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(months=6))
                if coursec.name == '年卡':
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(years=1))

            if coursec.card_type == 'sk':
                if coursec.nums == 1:
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(days=1))
                if coursec.nums == 10:
                    UserCourseCard.objects.filter(user=request.user,coursecard=coursec).update(has_time=datetime.datetime.now() + datetime.timedelta(years=1))


            coursecard = CourseCard.objects.get(id=int(coursecard_id))
            return render(request, "org-coursecard-detail.html",{
             "coursecard":coursecard,
             "buy_tip": "课卡购买成功！",
            })

        coursecard = CourseCard.objects.get(id=int(coursecard_id))
        return render(request, "org-coursecard-detail.html", {
            "coursecard": coursecard,
        })

class NoticDetailView(View):
    def get(self, request,notic_id, *args, **kwargs):
        notic = Notic.objects.get(id=int(notic_id))

        return render(request, "notic-detail.html",{
            "notic":notic,
        })


class OrgCourseCardView(View):
    def get(self, request, *args, **kwargs):
        coursecard_num = CourseCard.objects.all().count()
        all_coursecards = CourseCard.objects.all().order_by("-add_time")

        # 对课卡类型进行筛选
        c_type = request.GET.get("kk", "")
        if c_type:
            all_coursecards= all_coursecards.filter(card_type=c_type)

        # 对课卡数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_coursecards, per_page=8, request=request)
        coursecards = p.page(page)

        return render(request, "org-coursecard.html",{
            "coursecard_num":coursecard_num,
            "all_coursecards":coursecards,
            "c_type":c_type,
        })


class OrgJchfPlayView(View):
    def get(self, request, jchf_id, *args, **kwargs):
        jchf = Jchf.objects.get(id=int(jchf_id))

        comments = JchfComments.objects.filter(jchf_id=jchf_id).order_by("-add_time")

        jchf_c = Jchf.objects.get(id=int(jchf_id))
        jchf_c.click_nums += 1
        jchf_c.save()

        return render(request, "org-jchf-play.html",{
            "jchf":jchf,
            "comments":comments,
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = JchfCommentsForm(request.POST)
        if comment_form.is_valid():
            jchf = comment_form.cleaned_data["jchf"]
            comments = comment_form.cleaned_data["comments"]

            comment = JchfComments()
            comment.user = request.user
            comment.comments = comments
            comment.jchf = jchf
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class OrgJchfView(View):
    def get(self, request,  *args, **kwargs):
        all_jchfs = Jchf.objects.order_by("-add_time")

        # 对精彩回放数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_jchfs, per_page=15, request=request)
        jchfs = p.page(page)
        return render(request, "org-jchf.html",{
            "all_jchfs":jchfs,
            "MEDIA_URL":MEDIA_URL,
        })


class OrgInfoView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.filter(~Q(id=3))[:2]
        org =  CourseOrg.objects.get(id=3)
        return render(request, "org-info.html",{
            "all_orgs":all_orgs,
            "org":org,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                org_fav = True
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html",{
            "teacher":teacher,
            "MEDIA_URL": MEDIA_URL,
            "teacher_fav":teacher_fav,
            "org_fav":org_fav,
            "hot_teachers":hot_teachers,
        })

class TeacherListView(View):
    def get(self, request, *args, **kwargs):

        # 从数据库获取
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        keyworks = request.GET.get("keywords", "")
        s_type = "teacher"
        if keyworks:
            all_teachers =  all_teachers.filter(Q(name__icontains=keyworks))

        #对讲师进行排序
        sort = request.GET.get("sort","")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 老师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, per_page=5, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "MEDIA_URL": MEDIA_URL,
            "teacher_nums": teacher_nums,
            "sort":sort,
            "hot_teachers":hot_teachers,
            "keyworks": keyworks,
            "s_type": s_type,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "MEDIA_URL": MEDIA_URL,
            "current_page": current_page,
            "has_fav": has_fav,
        })

class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_course = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 对机构的课程数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, per_page=4, request=request)
        # per_page是控制每页多少个数
        courses = p.page(page)

        return render(request, "org-detail-course.html", {
            "all_course": courses,
            "course_org": course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })

class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teacher = course_org.teacher_set.all()

        # 对机构的老师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, per_page=2, request=request)
        # per_page是控制每页多少个数
        teachers = p.page(page)

        return render(request, "org-detail-teachers.html", {
            "all_teacher": teachers,
            "course_org": course_org,
            "MEDIA_URL": MEDIA_URL,
            "current_page":current_page,
            "has_fav": has_fav,
        })



class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:2]

        return render(request, "org-detail-homepage.html", {
            "all_course": all_course,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "MEDIA_URL": MEDIA_URL,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddAskView(View):
    """
    处理用户的咨询
    """
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg":"信息添加出错"
            })

class OrgView(View):
    def get(self, request, *args, **kwargs):
        #从数据库获取
        all_orgs = CourseOrg.objects.all().filter(~Q(id=3))
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        keyworks = request.GET.get("keywords", "")
        s_type = "org"
        if keyworks:
            all_orgs = all_orgs.filter(Q(name__icontains=keyworks) | Q(desc__icontains=keyworks))

        # 对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
           if city_id.isdigit():
               all_orgs = all_orgs.filter(city_id=int(city_id))

        #对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html",{
            "all_orgs":orgs,
            "MEDIA_URL":MEDIA_URL,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category":category,
            "city_id":city_id,
            "sort":sort,
            "hot_orgs":hot_orgs,
            "keyworks":keyworks,
             "s_type":s_type,
        })