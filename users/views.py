from rest_framework import generics

from .utils import *


class RegistrationView(APIView):
    """
    Registration
    """

    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess()
        else:
            return ResponseFail(serializer.errors)


class LoginUserView(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = []

    def get(self, request):
        """
        Profile view
        """
        serializer = UserEditSerialzier(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(
                {
                    'user': UserSerializer(request.user, context={'request': request}).data
                }
            )

    def put(self, request):
        serializer = UserEditSerialzier(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(
                {
                    'user': UserSerializer(request.user, context={'request': request}).data
                }
            )

        return ResponseFail(serializer.errors)


class ChangePasswordView(APIView):
    """
    Changing Password
    """

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors)

        user.set_password(serializer.validated_data.get('new_password'))
        user.save()

        password_changed(serializer.validated_data['new_password'], request.user)

        return ResponseSuccess


class UserListView(ListAPIViewResponseMixin, ListAPIView):
    field = 'users'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


class UserView(RetrieveAPIViewResponseMixin, RetrieveAPIView):
    field = 'user'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


class LogoutView(APIView):
    def get(self, request):
        return ResponseSuccess()
