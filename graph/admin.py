from django.contrib import admin


from .models import InstaCategories
from .models import UserInfo
from .models import LikingPreferences
from .models import InstaHistory
from .models import LikeHistory


class InstaCategoriesAdmin(admin.ModelAdmin):
    list_display = ('catname', 'catarray')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('accountuser', 'instauser', 'instapass', 'clientid', 'accesstoken', 'startdate')


class LikingPreferencesAdmin(admin.ModelAdmin):
    list_display = ('accountuser', 'likesperhour', 'consecutivehours', 'likesperday', 'subscribedcategories', 'enforceclarifai', 'enforcebanned', 'minposts', 'maxfollowers', 'minfollowers')

class InstaHistoryAdmin(admin.ModelAdmin):
    list_display = ('accountuser', 'uploads', 'totalfollowers', 'totalfollows', 'date')
    list_filter = ('accountuser',)

class LikeHistoryAdmin(admin.ModelAdmin):
    list_display = ('accountuser', 'username', 'link', 'date')


admin.site.register(InstaCategories, InstaCategoriesAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(LikingPreferences, LikingPreferencesAdmin)
admin.site.register(InstaHistory, InstaHistoryAdmin)
admin.site.register(LikeHistory, LikeHistoryAdmin)
