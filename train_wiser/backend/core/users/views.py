from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import RegisterSerializer, UserAccountSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.auth is None:
            data = request.data

            serializer = RegisterSerializer(data=data)

            if serializer.is_valid():
                try:
                    user = serializer.save()
                    return Response({'user_id' : user.id}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": "User is already authenticated"}, status=status.HTTP_403_FORBIDDEN)


# class UserAccount(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserAccountSerializer
#
#     def get_object(self):
#         username = self.kwargs['username']
#         return CustomUser.objects.get(username=username)


class UserAccount(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
