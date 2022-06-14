from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Group, GroupMembership, SnsUser
from rest_framework.decorators import api_view
from rest_framework import status as status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from sns.apps.order.models import Order
from sns.apps.order.serializers import OrderGroupSerializer, OrderProductSerializer, OrderSerializer

from django.db.models import Value, CharField
from sns.apps.invite.models import Invite
from .models import Group, GroupMembership
from sns.apps.invite.serializers import InviteSerializer
from .serializers import GroupMembershipSerializer, UserSerializer, AuthTokenSerializer, GroupSerializer, GroupStatusSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CustomCreateTokenView(ObtainAuthToken):
    """Create new auth token, that returns user information alongwith the token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super(CustomCreateTokenView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = SnsUser.objects.get(id=token.user_id)
        return Response({'token': token.key, 'id': token.user_id, 'name': user.name, 'email': user.email})


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class GetUserByIdViewSet(viewsets.ModelViewSet):
    """Get user information of other users by id"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SnsUser.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id',)
    http_method_names = ['get']

    def get_queryset(self):
        """Return all users based on filters"""
        id = str(self.request.query_params.get('id', ''))
        queryset = self.queryset
        if id:
            queryset = queryset.filter(id__iexact=id)
        return queryset.distinct()


class GroupViewSet(viewsets.ModelViewSet):
    """Manage Community groups"""
    serializer_class = GroupSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'city', 'type',)

    def get_queryset(self):
        """Return all group objects based on filters"""
        city = str(self.request.query_params.get('city', ''))
        type = str(self.request.query_params.get('type', ''))
        queryset = self.queryset
        if city:
            queryset = queryset.filter(city__icontains=city)
        if type:
            queryset = queryset.filter(type__iexact=type)
        return queryset.order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new group"""
        group = serializer.save()
        # Update the group membership table
        GroupMembership.objects.create(userid=self.request.user, groupid=group, isadmin=True)


class GroupMembershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage group membership"""
    serializer_class = GroupMembershipSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = GroupMembership.objects.all()

    def get_queryset(self):
        """Get all group details for current user"""
        return self.queryset.filter(
            userid=self.request.user.id
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_home_details(request,userid):

    try:
    
        summaryData={}

        # number of order completed 
        ordercomplete = Order.objects.filter(status='completed',acceptedby=userid).count()
        summaryData['ordercompleted'] = ordercomplete

        # order placed
        orderplaced = Order.objects.filter(status='completed',orderedby=userid).count()
        summaryData['orderplaced']=orderplaced

        #tip given
        tipgiven = Order.objects.filter(status='completed',orderedby=userid)
        
        tipgiven = sum(tipgiven.values_list('tipamount', flat=True))
        summaryData['tipgiven'] = tipgiven

        #tip received
        tipreceived = Order.objects.filter(status='completed',acceptedby=userid)
        
        tipreceived = sum(tipreceived.values_list('tipamount', flat=True))
        summaryData['tipreceived'] = tipreceived

        #wallet amount 
        walletamount = SnsUser.objects.get(id=userid).walletamount
        summaryData['walletamount']= walletamount


        return JsonResponse(summaryData, status= status.HTTP_200_OK,safe=False)
    
    except Exception as e:
        return JsonResponse({"error":"internal error occurred for getting stores"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GetUserGroupInviteAndMembershipDetails(viewsets.ModelViewSet):
    """Get user information of other users by id"""
    serializer_class = GroupStatusSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all().annotate(status=Value('Join', output_field=CharField()))
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city',)
    http_method_names = ['get']

    def get_queryset(self):
        """Return all users based on filters"""
        city = str(self.request.query_params.get('city', ''))
        queryset = self.queryset
        if city:
            queryset = queryset.filter(city__icontains=city)
        # get all group details by filter
        queryset = queryset.distinct()

        queryset_membership = GroupMembership.objects.filter(userid=self.request.user.id)
        queryset_invite = Invite.objects.filter(userid=self.request.user.id)

        for group in queryset:
            # Check if a given user is already a member of this group
            queryset_membership_check = queryset_membership.filter(groupid=group.id)
            queryset_invite_check = queryset_invite.filter(groupid=group.id)

            if queryset_membership_check:
                group.status = 'Approved'
            if queryset_invite_check:
                group.status = 'Pending'
			
        return queryset


class JoinGroupViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupMembershipSerializer
    queryset = GroupMembership.objects.all()

    def get_serializer_class(self):
        from rest_framework.exceptions import ValidationError
        data = self.request.data
        self.request.data["userid"] = self.request.user.id
        if "groupid" not in data:
            raise ValidationError({
                "groupid": "No group id provided to join" 
            })
        try:
            group = Group.objects.get(id=data["groupid"])
            if group.type == 'public':
                return GroupMembershipSerializer
            elif group.type == 'private':
                return InviteSerializer
            
            return self.serializer_class
        except Group.DoesNotExist:
            return self.serializer_class


    def create(self, request, *args, **kwargs):
        """Trying to join the group"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            group = Group.objects.get(id=self.request.data["groupid"])
            if group.type == 'public':
                # Check if the user, group pair already exists
                check_exists = GroupMembership.objects.filter(userid=self.request.user.id, groupid=group.id)
                if check_exists:
                    return Response({'Message': 'User already a member of this group'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
                GroupMembership.objects.create(userid=self.request.user, groupid=group, isadmin=False)

            elif group.type == 'private':
                check_exists = Invite.objects.filter(userid=self.request.user.id, groupid=group.id)
                if check_exists:
                    return Response({'Message': 'Invite to join this group already sent'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                Invite.objects.create(userid=self.request.user, groupid=group)

        except Group.DoesNotExist:
            return Response({'Message': 'Group with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
