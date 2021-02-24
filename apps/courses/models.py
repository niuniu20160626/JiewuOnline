from django.db import models

from DjangoUeditor.models import UEditorField
from apps.users.models import BaseModel, UserProfile
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
from datetime import datetime
# Create your models here.
# 1.设计表结构有几个重要的点


'''
实体1《关系》实体2
课程   章节   视频   课程资源
之间是一对多的关系

Course 课程信息
Lesson 章节信息
Video 视频
CourseResource 课程资源

在开发中不要直接使用Model类

2.找到实体的具体字段
3.每个字段的类型，是否必要填写
课程的评论也是一对多的情况
用户对课程进行收藏
'''

class AgeLay(BaseModel):
    age = models.CharField(default=10,null=False,max_length=20, verbose_name="年龄段")
    desc = models.CharField(max_length=200, verbose_name="描述")

    class Meta:
        verbose_name = "年龄段"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.age


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="老师")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="旗下分店")
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    start_time = models.DateTimeField(default=datetime.now, null=False,verbose_name="上课时间")
    learn_times = models.IntegerField(default=0, verbose_name="时长（分钟数）")
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    apoint_nums = models.IntegerField(default=0, verbose_name='预约人数')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name='课程价格')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")
    category = models.CharField(verbose_name="舞的种类", choices=(("ds", "URBAN DANCE(都市编舞)"), ("js", "JAZZ(爵士舞)"), ("zy", "HIPHOP(自由传统街舞)"), ("jx", "POPPING(机械舞 震感舞)")),max_length=20)
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    is_classics = models.BooleanField(default=False, verbose_name="是否经典")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/images/",filePath="courses/ueditor/files/", default="")
    is_banner = models.BooleanField(default=False, verbose_name="是否广告位")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    age = models.ForeignKey(AgeLay, on_delete=models.CASCADE,verbose_name="年龄段")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    #在后台中显示自己定义的列
    """
    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))
    show_image.short_description = "图片"
    """

# 课程学员
class CourseStudent(BaseModel):
    user = models.ForeignKey(UserProfile, null=True, blank=True,on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, null=True, blank=True,on_delete=models.CASCADE, verbose_name="课程")
    teacher_name = models.CharField(max_length=20, default="老师", unique=True, verbose_name="老师名称")
    is_apoints = models.BooleanField(default=False, verbose_name="是否预约")
    detail = models.CharField(max_length=200, default="无", verbose_name="备注")

    class Meta:
        verbose_name = "课程学员"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.course.name

class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True

class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag

class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")  # on_delete表示对应的外键数据被删除后，当前的数据应该怎么办
    name = models.CharField(max_length=100, verbose_name="课时名")
    learn_times = models.IntegerField(default=0, verbose_name="时长（分钟数）")

    class Meta:
        verbose_name = "课时信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="课时")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name="访问地址")

    class Meta:
        verbose_name = "教学回放视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
