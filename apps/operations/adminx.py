import xadmin

from apps.operations.models import UserAsk, UserCourse, UserFavorite, UserMessage, CourseComments, UserOrder, \
    JchfComments, UserCardOrder, UserCourseCard

from apps.operations.models import Banner
from import_export import resources


# 用户课程订单数据的导入导出
class MyUserCardOrder(resources.ModelResource):
    class Meta:
        model = UserCardOrder
        # fields = ('name', 'description',)
        # exclude = ()

class UserCardOrderAdmin(object):
    import_export_args = {'import_resource_class': MyUserCardOrder, 'export_resource_class': MyUserCardOrder}
    list_display = ['id', 'add_time', 'user','coursecard','price']
    search_fields = ['id', 'add_time', 'user','coursecard','price']
    list_filter = ['id', 'add_time', 'user','coursecard','price']

    model_icon = "fa fa-bars"

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(status=2)
        return qs


# 用户课程订单数据的导入导出
class MyUserOrder(resources.ModelResource):
    class Meta:
        model = UserOrder
        # fields = ('name', 'description',)
        # exclude = ()

class UserOrderAdmin(object):
    import_export_args = {'import_resource_class': MyUserOrder, 'export_resource_class': MyUserOrder}
    list_display = ['id', 'add_time', 'user','course','price']
    search_fields = ['id', 'add_time', 'user','course','price']
    list_filter = ['id', 'add_time', 'user','course','price']

    model_icon = "fa fa-bars"

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(status=2)
        return qs

# 轮播图数据的导入导出
class MyBanner(resources.ModelResource):
    class Meta:
        model = Banner
        # fields = ('name', 'description',)
        # exclude = ()

class BannerAdmin(object):
    import_export_args = {'import_resource_class': MyBanner, 'export_resource_class': MyBanner}
    list_display = ['title', 'image', 'url','index']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index']

    model_icon = "fa fa-file-image-o"

# 用户咨询数据的导入导出
class MyUserAsk(resources.ModelResource):
    class Meta:
        model = UserAsk
        # fields = ('name', 'description',)
        # exclude = ()

class UserAskAdmin(object):
    import_export_args = {'import_resource_class': MyUserAsk, 'export_resource_class': MyUserAsk}
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']

    model_icon = "fa fa-envelope-open-o"

# 用户课卡数据的导入导出
class MyUserCourseCard(resources.ModelResource):
    class Meta:
        model = UserCourseCard
        # fields = ('name', 'description',)
        # exclude = ()

class UserCourseCardAdmin(object):
    import_export_args = {'import_resource_class': MyUserCourseCard, 'export_resource_class': MyUserCourseCard}
    list_display = ['user', 'coursecard', 'has_time']
    search_fields = ['user', 'coursecard']
    list_filter = ['user', 'coursecard', 'has_time']

    model_icon = "fa fa-graduation-cap"


# 用户课程数据的导入导出
class MyUserCourse(resources.ModelResource):
    class Meta:
        model = UserCourse
        # fields = ('name', 'description',)
        # exclude = ()

class UserCourseAdmin(object):
    import_export_args = {'import_resource_class': MyUserCourse, 'export_resource_class': MyUserCourse}
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']

    model_icon = "fa fa-graduation-cap"

    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students += 1
            course.save()

# 用户消息数据的导入导出
class MyMessage(resources.ModelResource):
    class Meta:
        model = UserMessage
        # fields = ('name', 'description',)
        # exclude = ()

class UserMessageAdmin(object):
    import_export_args = {'import_resource_class': MyMessage, 'export_resource_class': MyMessage}
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']

    model_icon = "fa fa-weixin"


# 用户精彩回放评论数据的导入导出
class MyJchfComments(resources.ModelResource):
    class Meta:
        model = JchfComments
        # fields = ('name', 'description',)
        # exclude = ()

class JchfCommentsAdmin(object):
    import_export_args = {'import_resource_class': MyJchfComments, 'export_resource_class': MyJchfComments}
    list_display = ['user', 'jchf', 'comments', 'add_time']
    search_fields = ['user', 'jchf', 'comments', 'add_time']
    list_filter = ['user', 'jchf', 'comments', 'add_time']

    model_icon = "fa fa-play-circle"


# 用户课程评论数据的导入导出
class MyCourseComments(resources.ModelResource):
    class Meta:
        model = CourseComments
        # fields = ('name', 'description',)
        # exclude = ()

class CourseCommentsAdmin(object):
    import_export_args = {'import_resource_class': MyCourseComments, 'export_resource_class': MyCourseComments}
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']

    model_icon = "fa fa-comments-o"

# 用户收藏数据的导入导出
class MyUserFavorite(resources.ModelResource):
    class Meta:
        model = UserFavorite
        # fields = ('name', 'description',)
        # exclude = ()

class UserFavoriteAdmin(object):
    import_export_args = {'import_resource_class': MyUserFavorite, 'export_resource_class': MyUserFavorite}
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']

    model_icon = "fa fa-heartbeat"


xadmin.site.register(JchfComments, JchfCommentsAdmin)
xadmin.site.register(UserCardOrder, UserCardOrderAdmin)
xadmin.site.register(UserOrder, UserOrderAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserCourseCard, UserCourseCardAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(Banner,BannerAdmin)