
from django.http import JsonResponse
from rest_framework import status
from .models import Invite
from sns.apps.user.models import Group, GroupMembership, SnsUser
from sns.apps.user.serializers import GroupMembershipSerializer, GroupSerializer, UserSerializer
from .serializers import InviteSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
# Create your views here.

def fetchGroupName(groupDetailSerialized):
    groupDetailSerialized  = list(groupDetailSerialized)
    for i in groupDetailSerialized:
        groupId = i['groupid']

        groupDetail = Group.objects.get(id=groupId)
        groupDetailResponse = GroupSerializer(groupDetail)
        i['name']=groupDetailResponse.data['name']

        

        inviteDetails = Invite.objects.filter(groupid_id=groupId)
        inviteDetailsResponse = InviteSerializer(inviteDetails,many=True)

        inviteDetailsResponse = list(inviteDetailsResponse.data)

        for j in inviteDetailsResponse:
            userId = j['userid']
            userDetails = SnsUser.objects.get(id=userId)
            userDetailsResponse = UserSerializer(userDetails)
            j['address']= userDetailsResponse.data['address']
            j['name']=userDetailsResponse.data['name']
            j['city']=userDetailsResponse.data['city']
            j['mobile'] = userDetailsResponse.data['mobile']
            j['email']=userDetailsResponse.data['email']

        i['pending']= inviteDetailsResponse    

def addGroupData(inviteDetailSerialized):
    inviteDetailSerialized = list(inviteDetailSerialized)

    for i in inviteDetailSerialized:
        groupid = i['groupid']
        groupDetail = Group.objects.get(id=groupid)
        groupDetailResponse = GroupSerializer(groupDetail)
        i['name']=groupDetailResponse.data['name']


# Created this API to get all the invites from DB
@api_view(['GET'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def all_invite(request):
    try:
        invite1 = Invite.objects.all()
        serializer = InviteSerializer(invite1, many=True)
        return JsonResponse(serializer.data, safe=False)

    except Exception:
        return JsonResponse({"error": "Problem occured"}, status=status.HTTP_400_BAD_REQUEST)


# Created this API to filter the invites by userid
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_invite_by_userid(request, userid):

    try:
        print(userid)
        inviteDetailResponse = Invite.objects.filter(status='pending',userid=userid)
        inviteDetailSerialized = InviteSerializer(inviteDetailResponse, many=True)

        for i in inviteDetailSerialized.data:
            groupId = i['groupid']
            groupDetail = Group.objects.get(id=groupId)
            groupDetailResponse = GroupSerializer(groupDetail)
            i['name']=groupDetailResponse.data['name']


        return JsonResponse(inviteDetailSerialized.data, status=200, safe=False)

    except Invite.DoesNotExist:
        return JsonResponse({"error": "No invites Found by this user"}, status=status.HTTP_404_NOT_FOUND)


# Created this API to filter the invites by groupid
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_invite_by_groupid(request, groupid):

    try:
        print(groupid)
        inviteDetailResponse = Invite.objects.filter(groupid=groupid)
        inviteDetailSerialized = InviteSerializer(inviteDetailResponse, many=True)

        return JsonResponse(inviteDetailSerialized.data, status=200, safe=False)
        
    except Invite.DoesNotExist:
        return JsonResponse({"error": "No invites Found on this group"}, status=status.HTTP_404_NOT_FOUND)

# This API is create a new entry in invite table
# This API will trigger when user hits the 'Request to Join' button on private groups

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def request_to_join(request):

    print(request.body)
    try:
        deserializedInvite = InviteSerializer(data=request.data)
        # print(type(deserializedStore))
        print(deserializedInvite.is_valid())

        if deserializedInvite.is_valid():
            deserializedInvite.save()
        else:
            print(deserializedInvite.errors)
            return JsonResponse({"error": "Incorrect data for post"}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"success": "Store added successfully"}, status=status.HTTP_201_CREATED)

    except Exception:
        return JsonResponse({"error": "Problem occurred"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_pending_invites(request,adminid):
    
    try:
    
        groupDataResponse = GroupMembership.objects.filter(userid=adminid,isadmin=True)
        groupDetailSerialized = GroupMembershipSerializer(groupDataResponse,many=True)
        print(groupDetailSerialized.data)
        fetchGroupName(groupDetailSerialized.data)

        return JsonResponse(groupDetailSerialized.data,status=status.HTTP_200_OK,safe=False)

    except GroupMembership.DoesNotExist:
        return JsonResponse({"error":"Groups not Found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal error occured for getting store"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)    


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def accept_reject_pending_invites(request,inviteid):
    
    try:
        decision = request.data['status']

        if decision=="accepted":
            groupData = {"groupid":request.data['groupid'],"userid":request.data['userid'], "isadmin":False}
            print(groupData)

            deserializedGroupMemberShip = GroupMembershipSerializer(data=groupData)

            if deserializedGroupMemberShip.is_valid():
                deserializedGroupMemberShip.save()
                print('data saved')
            else:
                print(deserializedGroupMemberShip.errors)
                return JsonResponse({"error":"Error happened in accepting decision"},status=status.HTTP_400_BAD_REQUEST,safe=False)        

            inviteData = Invite.objects.get(id=inviteid)
            inviteData.delete()
              

            return JsonResponse({"success":"Invited accepted successfully"},status=status.HTTP_200_OK,safe=False)    

        #rejected status    
        else:
            print('invite rejected and deleted prcess start',inviteid)

            inviteData = Invite.objects.get(id=inviteid)
            inviteData.delete()
            
            print('invite rejected and deleted')

            return JsonResponse({"success":"Invited rejected successfully"},status=status.HTTP_200_OK,safe=False)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal error occured for decision of invite "},status=status.HTTP_503_SERVICE_UNAVAILABLE)            
