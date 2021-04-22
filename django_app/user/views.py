from django.shortcuts import get_object_or_404
from instagram_app import permissions as up
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from rest_framework.authtoken.models import Token


class AuthLoginLogout(APIView):
    permission_classes = (
            up.IsMethodPost |
            up.IsMethodDelete & permissions.IsAuthenticated,
    )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            raise ValueError('can\'t find username')
        if not password:
            raise ValueError('can\'t find password')

        user_instance = get_object_or_404(User, username=username)
        try:
            if user_instance.check_password(password):
                user_token, created = Token.objects.get_or_create(user=user_instance)
                return Response(user_token.key)
            else:
                raise ValueError('password 땡')
        except ValueError as e:
            return Response(f'{e}')

    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response()


class SignUpWithdrawal(APIView):
    permission_classes = (
            up.IsMethodPost |
            up.IsMethodDelete & permissions.IsAuthenticated,
    )

    def post(self, request):
        necessary_fields = {'username', 'password', 'name'}
        all_fields = {'username', 'password', 'name', 'description'}
        for key in request.data:
            if key not in all_fields:
                return Response('잘못된 값을 전달했습니다.')
        for necessary in necessary_fields:
            if necessary not in request.data:
                return Response(f'{necessary}값을 입력해주세요')

        try:
            if User.objects.filter(username=request.data['username']).exists():
                raise Exception(f'해당 ID는 이미 존재합니다')
        except Exception as e:
            return Response(f'에러가 발생했습니다. {e}')

        User.objects.create(**request.data)

        return Response()

    def delete(self, request):
        User.objects.get(id=request.user.id).delete()
        return Response()
