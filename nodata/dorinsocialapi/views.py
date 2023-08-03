from rest_framework import (
    generics, 
    status, 
    serializers, 
    permissions
)
from rest_framework.response import Response


from dorin.models import (
    Profile,
    Post,
)


from dorinsocialapi.serializers import (
    ProfileBasicSerializer,
    ProfileDetailSerializer,
    PostSerializer,
)
from dorinsocialapi.mixins import (
    UserQuerySetMixin,
)
from dorinsocialapi.permissions import IsStaffOrOwnerPermission



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
