from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializers import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from server.schema import server_list_docs


# Create your views here.


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        category = request.GET.get("category_id")
        by_user = request.GET.get("by_user", None) == "true"
        qty = request.GET.get("qty")
        by_server_id = request.GET.get("server_id")
        with_num_members = request.GET.get("with_num_members") == "true"

        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail="Server with id does not exist")
            except ValueError:
                raise ValidationError(detail="Not a valid Server id")

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
