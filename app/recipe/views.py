from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from .serializers import TagSerializer



class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """manage tags in db"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """return objects for only authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')