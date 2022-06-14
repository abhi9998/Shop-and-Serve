from django.urls import path
from .views import accept_reject_pending_invites, all_invite, get_invite_by_groupid, get_invite_by_userid, request_to_join, show_pending_invites

urlpatterns = [
    path("api/invite/", all_invite),
    path("api/invite/user/<userid>", get_invite_by_userid),
    path("api/invite/joinGroup", request_to_join),
    path("api/invite/group/<groupid>", get_invite_by_groupid),
    path("api/invite/admin/<adminid>",show_pending_invites),
    path("api/invite/decision/<inviteid>",accept_reject_pending_invites)
    ]
