from import_export import resources

import xadmin

from apps.organizations.models import Teacher, CourseOrg, City, Jchf, Notic, CourseCard


# 课卡数据的导入导出
class MyCourseCard(resources.ModelResource):
    class Meta:
        model = CourseCard
        # fields = ('name', 'description',)
        # exclude = ()

class CourseCardAdmin(object):
    import_export_args = {'import_resource_class': MyCourseCard, 'export_resource_class': MyCourseCard}
    list_display = ["card_type", "name", "nums", "price","has_time"]
    search_fields = ["card_type", "name", "nums", "price","has_time"]
    list_filter = ["card_type", "name", "nums", "price","has_time"]
    list_editable = ["card_type", "name", "nums", "price","has_time"]

    "图标"
    model_icon = "fa fa-address-card"


# 网站公告数据的导入导出
class MyNotic(resources.ModelResource):
    class Meta:
        model = Notic
        # fields = ('name', 'description',)
        # exclude = ()


class NoticAdmin(object):
    import_export_args = {'import_resource_class': MyNotic, 'export_resource_class': MyNotic}
    list_display = ["title", "desc"]
    search_fields = ["title", "desc"]
    list_filter = ["title", "desc"]
    list_editable = ["title", "desc"]

    style_fields = {
        "desc": "ueditor"
    }

    "图标"
    model_icon = "fa fa-address-card"


# 精彩回放数据的导入导出
class MyJchf(resources.ModelResource):
    class Meta:
        model = Jchf
        # fields = ('name', 'description',)
        # exclude = ()


class JchfAdmin(object):
    import_export_args = {'import_resource_class': MyJchf, 'export_resource_class': MyJchf}
    list_display = ["title", "desc", "url", "click_nums"]
    search_fields = ["title", "desc", "url", "click_nums"]
    list_filter = ["title", "desc", "url", "click_nums"]
    list_editable = ["title", "desc", "url", "click_nums"]

    "图标"
    model_icon = "fa fa-address-card"


# 老师数据的导入导出
class MyTeacher(resources.ModelResource):
    class Meta:
        model = Teacher
        # fields = ('name', 'description',)
        # exclude = ()


class TeacherAdmin(object):
    import_export_args = {'import_resource_class': MyTeacher, 'export_resource_class': MyTeacher}
    list_display = ["org", "name", "work_years", "work_company"]
    search_fields = ["org", "name", "work_years", "work_company"]
    list_filter = ["org", "name", "work_years", "work_company"]
    list_editable = ["org", "name", "work_years", "work_company"]

    "图标"
    model_icon = "fa fa-address-card"


#课程机构的导入导出
class MyCourseOrg(resources.ModelResource):
    class Meta:
        model = CourseOrg
        # fields = ('name', 'description',)
        # exclude = ()


class CourseOrgAdmin(object):
    import_export_args = {'import_resource_class': MyCourseOrg, 'export_resource_class': MyCourseOrg}
    list_display = ["name", "desc", "click_nums","fav_nums"]
    search_fields = ["name", "desc", "click_nums","fav_nums"]
    list_filter = ["name", "desc", "click_nums","fav_nums"]
    list_editable = ["name", "desc", "click_nums","fav_nums"]

    style_fields = {
        "desc": "ueditor"
    }

    model_icon = "fa fa-users"


#课程机构的导入导出
class MyCity(resources.ModelResource):
    class Meta:
        model = City
        # fields = ('name', 'description',)
        # exclude = ()


class CityAdmin(object):
    import_export_args = {'import_resource_class': MyCity, 'export_resource_class': MyCity}
    list_display = ["id", "name", "desc", "add_time"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]
    list_editable = ["name", "desc"]

    model_icon = "fa fa-location-arrow"


xadmin.site.register(CourseCard, CourseCardAdmin)
xadmin.site.register(Notic, NoticAdmin)
xadmin.site.register(Jchf, JchfAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)