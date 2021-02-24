import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render

from django.views.generic.base import View

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from pure_pagination import Paginator

from apps.courses.models import Course
from apps.operations.models import UserFavorite, UserMessage, Banner, UserOrder, UserCardOrder
from apps.organizations.models import CourseOrg, Teacher
from apps.users.forms import LoginForm, DynamicLoginForm, RegisterPostForm, ChangePwdForm, UpdateMobileForm
from apps.utils.YunPian import send_single_sms
from JiewuOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.forms import DynamicLoginPostForm
from apps.users.models import UserProfile
from apps.users.forms import RegisterGetForm
from apps.users.forms import UploadImageForm,UserInfoForm


class MyOrderView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        orders = UserOrder.objects.filter(user=request.user,status=2).order_by('-add_time')
        cardorders = UserCardOrder.objects.filter(user=request.user, status=2).order_by('-add_time')
        current_page = "myorder"

        # 对课程订单数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(orders, per_page=3, request=request)
        orders = p.page(page)

        # 对课卡订单数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(cardorders, per_page=3, request=request)
        cardorders = p.page(page)

        return render(request, "usercenter-myorder.html", {
            "orders": orders,
            "cardorders":cardorders,
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        #删除订单
        order_id = request.POST.get("order_id")
        cardorder_id = request.POST.get("cardorder_id")
        if order_id:
            UserOrder.objects.filter(id=(order_id)).delete()
            return JsonResponse({
            "status": "success",
            "msg": "已经删除"
            })

        if cardorder_id:
            UserCardOrder.objects.filter(id=int(cardorder_id)).delete()
            return JsonResponse({
                "status": "success",
                "msg": "已经删除"
            })

#未读消息
def message_nums(request):
    """
    Add media-related context variables to the context.
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user).order_by('-add_time')
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()

        # 对消息数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=5, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html",{
            "messages":messages,
            "current_page":current_page
        })



class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html",{
            "course_list":course_list,
            "current_page":current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, "usercenter-fav-teacher.html",{
            "teacher_list":teacher_list,
            "current_page":current_page
        })

class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html",{
            "org_list":org_list,
            "current_page":current_page
        })

"""
class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        #通过反向取(user.usercourse_set.alll)也可以拿到 user_course
        #my_courses = UserCourse.objects.filter(user=request.user)

        return render(request, "usercenter-mycourse.html",{
            #"my_courses":my_courses,
            "current_page":current_page,
        })
"""

#修改手机号
class ChangeMobileView(LoginRequiredMixin,View):

    login_url = "/login/"
    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            #已经存在的记录不能复注册
            if request.user.mobile == mobile:
                return JsonResponse({
                    "mobile": "和当前号码一致"
                })

            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile":"该手机号码已经被注册"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)




#修改密码
class ChangePwdView(LoginRequiredMixin,View):
    login_url = "/login/"
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
               return JsonResponse({
                   "status":"fail",
                   "msg":"密码不一致"
               })

            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request, user)
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(pwd_form.errors)


#修改头像
class UploadImageView(LoginRequiredMixin,View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        #处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        #同一个文件上传多次，相同名称的文件应该如何处理
        #文件的保存路径应该保存到user
        #表单验证
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

#修改信息
class UserInfoView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        captcha_form = RegisterGetForm()
        current_page = "info"
        return render(request,"usercenter-info.html",{
            "captcha_form":captcha_form,
            "current_page":current_page,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status":"fail"
            })




class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        banners = Banner.objects.all()[:3]
        return render(request, "register.html",{
            "register_get_form":register_get_form,
            "banners":banners,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        banners = Banner.objects.all()[:3]
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 验证手机号和短信验证码已经在forms里面验证了
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form,
                "banners":banners,
            })


class DynamicLoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        banners = Banner.objects.all()[:3]
        return render(request, "login.html",{
            "login_form":login_form,
            "next":next,
            "banners":banners,
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():# 没有注册账号依然可以使用
           mobile = login_form.cleaned_data["mobile"]
           existed_users = UserProfile.objects.filter(mobile=mobile)
           if existed_users:
               user = existed_users[0]
           else:
               #新建用户
               user = UserProfile(username=mobile)
               # 随机生成密码
               password = generate_random(10, 2)
               user.set_password(password)
               user.mobile = mobile
               user.save()
           login(request, user)
           next = request.GET.get("next", "")
           if next:
               return HttpResponseRedirect(next)
           return HttpResponseRedirect(reverse("index"))
        else:
            # 如何将表单验证的error显示到HTML中
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": d_form,
                                                  "dynamic_login": dynamic_login,
                                                  "banners":banners,})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            #随机生成验证码
            code = generate_random(4,0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile),code)
                r.expire(str(mobile),60*5) #设置验证码五分钟过期
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # 返回界面，在urls中不在写入 template_name = "login.html"
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        # 返回界面，在urls中不在写入 template_name = "login.html"
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        #返回登录状态
        request.session['next'] = request.META.get('HTTP_REFERER', '/')
        next = request.GET.get("next", "")

        banners = Banner.objects.all()[:3]

        login_form = DynamicLoginForm()
        return render(request, "login.html",{
            "login_form":login_form,
            "next":next,
            "banners": banners
        })

    def post(self, request, *args, **kwargs):
        # 完成数据的获取
        # 表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            # user_name = request.POST.get("username","")
            # password = request.POST.get("password","")
            # 登录逻辑
            # 用于通过用户和密码查询用户是否存在
            # 验证字段
            # if not user_name:
            # return render(request, "login.html", {"msg": "请输入用户名"})

            # if not password:
            #    return render(request, "login.html",{"msg": "请输入密码"})

            # if len(password) < 8:
            #   return render(request, "login.html", {"msg": "密码格式不正确"})
            # from apps.users.models import UserProfile
            # 1.通过用户查询到用户
            # 2.查询需要先加密，然后通过加密之后的密码查询
            # user = UserProfile.objects.get(username=user_name, password = password)
            if user is not None:
                # 查询到用户,登录方法
                # 登录成功，要返回首页
                # 前端request拿到user对象
                # 在template中有
                # cookie 和 session 原理，保存状态
                login(request, user)

                #登录之后应该怎么返回页面
                next = request.session['next']
                if next:
                    return HttpResponseRedirect(next)

                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户
                return render(request, "login.html", {"msg": "用户名或密码错误！", "login_form": login_form,"banners": banners})
        else:
            # 如何将表单验证的error显示到HTML中
            return render(request, "login.html", {"login_form": login_form,"banners": banners})