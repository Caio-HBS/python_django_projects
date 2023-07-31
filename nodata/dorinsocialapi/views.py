from rest_framework import generics, status, serializers
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


class ProfileListAPIView(generics.ListAPIView):
    # TODO: Implement high level security to allow only admin to see this view, 
    #       otherwise return only the user object (if logged).
    """
        API view to retrieve a list of user profiles.

        Inherits from DRF's ListAPIView, providing a read-only endpoint
        to fetch a collection of user profiles.

        Endpoint URL: /dorinsocialapi/profiles/
        HTTP Methods Allowed: GET
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    # TODO: Implement security so that only logged in users with permission will
    #       be able to see/edit this.
    """
        API view to retrieve a single user profile.

        Inherits from DRF's RetrieveAPIView, providing a read-only endpoint
        to fetch details of a specific user profile.

        Endpoint URL: /dorinsocialapi/profiles/<int:pk>/
        HTTP Methods Allowed: GET
    """
    serializer_class = ProfileDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Profile.objects.prefetch_related('posts').all()
        return queryset


class ProfileUpdateAPIView(generics.UpdateAPIView):
    # TODO: Implement security so that only authorized users or the owner of the
    #       profile can use this endpoint.
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
    


class ProfileDestroyAPIView(generics.DestroyAPIView):
    # TODO: Implement security so that only authorized users or the owner of the
    #       profile can use this endpoint.
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
    # TODO: Implement security so that only authorized users and the owner of the
    #       profile can see this.
    """
        API view to list and create posts.

        Inherits from DRF's ListCreateAPIView, providing an endpoint to
        retrieve a list of posts and create new posts.

        Endpoint URL: /dorinsocialapi/posts/
        HTTP Methods Allowed: GET, POST
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        choosen_pk_for_profile = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=choosen_pk_for_profile)
        except Profile.DoesNotExist:
            return Post.objects.none()

        queryset = Post.objects.all().filter(parent_profile=profile)
        return queryset

    def perform_create(self, serializer):
        choosen_pk_for_profile = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=choosen_pk_for_profile)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Couldn't find this profile")

        serializer.is_valid(raise_exception=True)
        serializer.save(parent_profile=profile)
