from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, CustomCreateTokenView, JoinGroupViewSet, ManageUserView, \
                    GroupViewSet, GroupMembershipViewSet, GetUserByIdViewSet, get_home_details, \
                    GetUserGroupInviteAndMembershipDetails

app_name = 'user'

router = DefaultRouter()
router.register('groups', GroupViewSet)
router.register('mygroups', GroupMembershipViewSet)
router.register('searchGroup', GetUserGroupInviteAndMembershipDetails)
router.register('joinGroup', JoinGroupViewSet)
router.register('otheruser', GetUserByIdViewSet)

urlpatterns = [
        path('', include(router.urls)),
        path('create', CreateUserView.as_view(), name='create'),
        path('login', CustomCreateTokenView.as_view(), name='login'),
        path('myprofile', ManageUserView.as_view(), name='myprofile'),
        path('home/<userid>',get_home_details)
]
