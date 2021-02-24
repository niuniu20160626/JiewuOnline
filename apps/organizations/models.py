import sys
from datetime import datetime
from django.db import models
from apps.users.models import BaseModel
from DjangoUeditor.models import UEditorField
# Create your models here.

'''
City 城市实体
CourseOrg  培训机构
Teacher 教师
'''


class CourseCard(BaseModel):
    card_type = models.CharField(default="ck", verbose_name="课卡类型", max_length=4, choices=(("ck", "次卡"), ("tk", "通卡"),("sk", "一对一课卡")))
    name = models.CharField(max_length=25, verbose_name="课卡名称")
    nums = models.IntegerField(default=sys.maxsize, verbose_name="次数")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='课卡价格')
    has_time = models.DateTimeField(default=datetime.now, null=False, verbose_name="有效期")
    desc = models.CharField(max_length=100,default="课卡的有效期从购买时开始算起",verbose_name="备注说明")
    image = models.ImageField(upload_to="org/coursecard/%Y/%m", verbose_name="封面", max_length=100)

    class Meta:
        verbose_name = "课卡"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Notic(BaseModel):
    title = models.CharField(max_length=25, verbose_name="公告标题")
    image = models.ImageField(upload_to="org/n/%Y/%m", null=True,verbose_name="封面", max_length=200)
    desc = UEditorField(verbose_name="描述", width=800, height=500, imagePath="org/ueditor/notic/images/",filePath="courses/ueditor/notic/files/", default="")

    class Meta:
        verbose_name = "网站公告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Jchf(BaseModel):
    title = models.CharField(max_length=25, verbose_name="回放标题")
    desc = models.CharField(max_length=100, verbose_name="回放描述")
    url = models.CharField(max_length=1000, verbose_name="访问地址")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    image = models.ImageField(upload_to="org/jchf/%Y/%m", null=True,verbose_name="封面", max_length=200)

    class Meta:
        verbose_name = "精彩回放"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=200, verbose_name="描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="分店名称")
    desc = UEditorField(verbose_name="描述", width=600, height=300, imagePath="courses/ueditor/images/",filePath="courses/ueditor/files/", default="")
    tag = models.CharField(default="长沙知名", max_length=10, verbose_name="分店标签")
    category = models.CharField(default="se", verbose_name="分店类别", max_length=4,choices=(("se", "少儿"), ("cr", "成人")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="分店地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    def courses(self):
        #from apps.courses.models import Course #这个要放这里
        #courses= Course.objects.filter(course_org=self)
        #外键反向取
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    class Meta:
        verbose_name = "旗下分店"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


from apps.users.models import UserProfile
class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="用户")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属分店")
    name = models.CharField(max_length=50, verbose_name="老师名")
    work_years = models.IntegerField(default=0, verbose_name="舞龄")
    work_company = models.CharField(max_length=50, verbose_name="就职分店")
    work_position = models.CharField(max_length=100, verbose_name="所教舞种")
    points = models.CharField(max_length=600, verbose_name="经历")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "老师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()

