from rest_framework import renderers
from rest_framework.utils import json
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class Pagination:
    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PaginationMethod(Pagination):

    def page(self, instance, serializers, request):
        page = super().paginate_queryset(instance)
        if page is not None:
            serializer = super().get_paginated_response(
                serializers(page, many=True, context={'request': request}).data
            )
        else:
            serializer = serializers(instance, many=True, context={'request': request})
        return serializer


class UserRenderers(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""
        if "ErrorDetail" in str(data):
            response = json.dumps({"errors": data})
        else:
            response = json.dumps(data)
        return response



def validate_file_size(value):
    max_size = 2 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            (f'File size must be no more than 2 mb.'),
            params={'max_size': max_size},
        )


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
      "refresh": str(refresh),
      "access": str(refresh.access_token)}