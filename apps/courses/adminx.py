import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse, CourseStudent, AgeLay
from xadmin.layout import Fieldset, Main, Side, Row
from import_export import resources

class GlobalSettings(object):#在某个应用下面的adminx 都可以
    site_title = "街舞培训后台管理系统"
    site_footer = "街舞培训网"
    menu_style = 'accordion'   #左边菜单是否收起来等操作风格


class BaseSettings(object):#在某个应用下面的adminx 都可以
    enable_themes = True #主题修改
    use_bootswatch = True #企图调出主题菜单，显示更多主题

#年龄段数据的导入导出
class MyAgeLay(resources.ModelResource):
    class Meta:
        model = AgeLay
        # fields = ('name', 'description',)
        # exclude = ()


class AgeLayAdmin(object):
    import_export_args = {'import_resource_class': MyAgeLay, 'export_resource_class': MyAgeLay}
    list_display = [ "id", "add_time", "age","desc"]
    search_fields = [ "id", "add_time", "age","desc"]
    list_filter = [ "id", "add_time", "age","desc"]
    model_icon = "fa fa-times-circle-o"

#课程学员数据的导入导出
class MyCourseStudent(resources.ModelResource):
    class Meta:
        model = CourseStudent
        # fields = ('name', 'description',)
        # exclude = ()

class CourseStudentAdmin(object):
    import_export_args = {'import_resource_class': MyCourseStudent, 'export_resource_class': MyCourseStudent}
    list_display = [ "id", "user", "course","teacher_name","is_apoints","detail"]
    search_fields = [ "id", "user", "course","is_apoints","detail"]
    list_filter = [ "id", "user", "course","is_apoints","detail"]
    model_icon = "fa fa-user-o"

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher_name=self.request.user.teacher.name)
        return qs


#课程轮播数据的导入导出
class MyBannerCourse(resources.ModelResource):
    class Meta:
        model = BannerCourse
        # fields = ('name', 'description',)
        # exclude = ()

class BannerCourseAdmin(object):
    import_export_args = {'import_resource_class': MyBannerCourse, 'export_resource_class': MyBannerCourse}
    list_display = [ "name", "desc", "detail","degree","learn_times","students"]
    search_fields = ["name", "desc", "detail","degree","students"]
    list_filter = [ "name", "teacher__name", "desc", "detail","degree","learn_times","students"]
    list_editable = ["degree", "desc"]

    model_icon = "fa fa-picture-o"
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonInline(object):
    model = Lesson
    style = "tab"
    #extra = 0

class CourseResourceInline(object):
    model = CourseResource
    style = "tab"
    extra = 1


#课程后台配置导入导出数据的
class MyResource(resources.ModelResource):
    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()

class NewCourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    #list_display = [ "name", "desc", "show_image", "detail","degree","learn_times","students"]
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students"]
    search_fields = ["name", "desc", "detail","degree","students"]
    list_filter = [ "name", "teacher__name", "desc", "detail","degree","learn_times","students"]
    list_editable = ["degree", "desc"]

    #限制哪些数据可以改，哪些不能改
    readonly_fields = ["add_time"]
    # readonly_fields 和 exclude 不能同时存在，必填的不要不能改和看不见
    #某些字段看不见
    exclude = ["click_nums", "fav_nums","students"]

    #进去就排序的
    ordering = ["-click_nums"]

    #图标
    model_icon = "fa fa-id-card-o"

    #在填加课程的时候，一起添加章节，需要有外键
    inlines = [LessonInline,CourseResourceInline]
    style_fields = {
        "detail": "ueditor"
    }

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    #后台修改数据时，数据显示的位置
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset("讲师信息",
                             'teacher', 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset("基本信息",
                             'name', 'desc',
                             Row('learn_times', 'degree'),
                             Row('category', 'tag'),
                             'youneed_know', 'teacher_tell', 'detail',
                             ),
                ),
               # Side(
                #    Fieldset("访问信息",
                 #            'fav_nums', 'click_nums', 'students', 'add_time'
                  #           ),
                #),
                Side(
                    Fieldset("选择信息",
                             'is_banner', 'is_classics'
                             ),
                )
            )
        return super(NewCourseAdmin, self).get_form_layout()

#课程标签数据的导入导出
class MyCourseTag(resources.ModelResource):
    class Meta:
        model = CourseTag
        # fields = ('name', 'description',)
        # exclude = ()

class CourseTagAdmin(object):
    import_export_args = {'import_resource_class': MyCourseTag, 'export_resource_class': MyCourseTag}
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']

    model_icon = "fa fa-tumblr"

#课程章节数据的导入导出
class MyLesson(resources.ModelResource):
    class Meta:
        model = Lesson
        # fields = ('name', 'description',)
        # exclude = ()

class LessonAdmin(object):
    import_export_args = {'import_resource_class': MyLesson, 'export_resource_class': MyLesson}
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']

    model_icon = "fa fa-bars"

#video数据的导入导出
class MyVideo(resources.ModelResource):
    class Meta:
        model = Video
        # fields = ('name', 'description',)
        # exclude = ()

class VideoAdmin(object):
    import_export_args = {'import_resource_class': MyVideo, 'export_resource_class': MyVideo}
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']

    model_icon = "fa fa-play-circle"

#课程资源数据的导入导出
class MyResourcer(resources.ModelResource):
    class Meta:
        model = CourseResource
        # fields = ('name', 'description',)
        # exclude = ()

class CourseResourceAdmin(object):
    import_export_args = {'import_resource_class': MyResourcer, 'export_resource_class': MyResourcer}
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']

    model_icon = "fa fa-file"


xadmin.site.register(AgeLay, AgeLayAdmin)
xadmin.site.register(CourseStudent, CourseStudentAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)#在某个应用下面的adminx 都可以
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)#在某个应用下面的adminx 都可以