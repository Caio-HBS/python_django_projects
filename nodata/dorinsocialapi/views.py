from rest_framework import generics, status, serializers
from rest_framework.response import Response


from dorin.models import (
    Profile,
    Post,
)

from dorinsocialapi.serializers import (
    ProfileSerializer,
    PostSerializer,
)


class ProfileListAPIView(generics.ListAPIView):
    # TODO: Implement high level security to allow only admin to see this view, 
    #       otherwise return only the user object (if logged).
    """
        Basic list view for profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    # TODO: Implement security so that only logged in users with permission will
    #       be able to see/edit this.
    # TODO: Implement nested retrieval for posts, likes and comments.
    """
        Profile detail view, including posts, likes and comments.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'


class ProfileUpdateAPIView(generics.UpdateAPIView):
    # TODO: Implement security so that only authorized users or the owner of the
    #       profile can use this endpoint.
    """
        Profile update view.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
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
        Profile destroy view (also deletes user, posts, comments and likes).
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
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
        Posts based on a single instance view.
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
            raise serializers.ValidationError("O perfil específico não existe.")

        serializer.is_valid(raise_exception=True)
        serializer.save(parent_profile=profile)

    # def create(self):
    #     return
    
    # def perform_create(self):
    #     return
    
