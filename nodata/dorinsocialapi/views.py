from django.utils import timezone

from rest_framework import (
    authentication,    
    generics,    
    permissions,    
    serializers,    
    status,
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


from dorin.models import (
    Post,
    Profile,
)

from dorinsocialapi.authentication import TokenAuthentication
from dorinsocialapi.mixins import UserQuerySetMixin
from dorinsocialapi.permissions import IsStaffOrOwnerPermission
from dorinsocialapi.serializers import (
    PostSerializer,
    ProfileBasicSerializer,
    ProfileDetailSerializer,
)



class CustomAuthTokenView(ObtainAuthToken):
    """
        Creates and provides a new token once the user is authenticated. If 
        authentication is met, provides both the token and user id for profile.
        Also provides new token if the old one is more than seven days old.

        Endpoint URL: /dorinsocialapi/get-auth-token//
        HTTP Methods Allowed: POST
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user)
            time_difference = timezone.now() - token.created
            token_valid_duration = timezone.timedelta(days=7)
        
            if time_difference > token_valid_duration:
                token.delete()
                token = Token.objects.create(user=user)
        
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
        })



class ProfileListAPIView(UserQuerySetMixin, generics.ListAPIView):
    """
        API view to retrieve a list of user profiles.

        Inherits from DRF's ListAPIView, providing a read-only endpoint
        to fetch a collection of user profiles.

        Endpoint URL: /dorinsocialapi/profiles/
        HTTP Methods Allowed: GET
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        TokenAuthentication, authentication.SessionAuthentication
    ]


class ProfileDetailAPIView(UserQuerySetMixin, generics.RetrieveAPIView):
    """
        API view to retrieve a single user profile.

        Inherits from DRF's RetrieveAPIView, providing a read-only endpoint
        to fetch details of a specific user profile.

        Endpoint URL: /dorinsocialapi/profiles/<int:pk>/
        HTTP Methods Allowed: GET
    """
    serializer_class = ProfileDetailSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        TokenAuthentication, authentication.SessionAuthentication
    ]
    queryset = Profile.objects.prefetch_related('posts').all()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """
        API view to update a user profile.

        Inherits from DRF's UpdateAPIView, providing an endpoint to update
        the details of a specific user profile.

        Endpoint URL: /dorinsocialapi/profiles/<int:pk>/update/
        HTTP Methods Allowed: PUT, PATCH
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated, IsStaffOrOwnerPermission]
    authentication_classes = [
        TokenAuthentication, authentication.SessionAuthentication
    ]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
    


class ProfileDestroyAPIView(generics.DestroyAPIView):
    """
        API view to delete a user profile (as well as all other user related 
        objects).

        Inherits from DRF's DestroyAPIView, providing an endpoint to delete
        a specific user profile.

        Endpoint URL: /dorinsocialapi/profiles/<int:pk>/delete/
        HTTP Methods Allowed: DELETE
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated, IsStaffOrOwnerPermission]
    authentication_classes = [
        TokenAuthentication, authentication.SessionAuthentication
    ]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Profile deleted successfully"
        },
        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        user_id = instance.user.id
        instance.user.delete()
        instance.delete()


class PostListCreateAPIView(generics.ListCreateAPIView):
    """
        API view to list and create posts.

        Inherits from DRF's ListCreateAPIView, providing an endpoint to
        retrieve a list of posts and create new posts.

        Endpoint URL: /dorinsocialapi/profiles/<int:pk>/posts/
        HTTP Methods Allowed: GET, POST
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        TokenAuthentication, authentication.SessionAuthentication
    ]



    def get_queryset(self):
        choosen_pk_for_profile = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=choosen_pk_for_profile)
        except Profile.DoesNotExist:
            return Post.objects.none()
        
        if not self.request.user.is_staff and profile.user != self.request.user:
            return Post.objects.none()

        queryset = Post.objects.all().filter(parent_profile=profile)
        return queryset

    def perform_create(self, serializer):
        choosen_pk_for_profile = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=choosen_pk_for_profile)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Couldn't find this profile")
        
        if not self.request.user.is_staff and profile.user != self.request.user:
            raise serializers.ValidationError(
                "You don't have permission to perform this action"
            )

        serializer.is_valid(raise_exception=True)
        serializer.save(parent_profile=profile)
