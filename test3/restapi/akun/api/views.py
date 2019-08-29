from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from akun.models import UserExtend

class RegisterUserAPIView(APIView):

    def post(self,request,*args,**kwargs):
        try:
            User.objects.create(
                username=self.request.data["username"],
                password=self.request.data["password"],
                email=self.request.data["email"],
            )
            UserExtend.objects.create(
                user=User.objects.get(username=self.request.data["username"]),
                city=self.request.data["city"],
                zipcode=self.request.data["zipcode"],
            )
            return Response({
                'message':'User dengan nama {} berhasil di buat'.format(self.request.data['username']),
            })
        except:
            return Response({
                'error':'Data yang anda masukkan belum lengkap',
            })

class ListUserAPIView(APIView):

    def get(self,request,*args,**kwargs):

        # Initializing Query Parameter
        try:
            sortParam=self.request.query_params["sort_by"]
            typeSort=self.request.query_params["type_sort"]
        except:
            sortParam="user_id"
            typeSort="asc"
        try:
            filterParam=self.request.query_params["filter_by"]
            filterValue=self.request.query_params["filter_value"]
        except:
            filterParam="user_id"
            filterValue=""

        # Query Parameter Processing
        # Pastikan filter_by atau sort_by nilainya berada di salah satu
        # Field di bawah ini
        field=["user_id","username","email","city","date_joined","zipcode"]
        if not sortParam in field:
            return Response({
                'error':"Masukkan Salah satu parameter sort_by di atas ini",
                "parameter":field
            },status=400)
        
        if not filterParam in field:
            return Response({
                'error':"Masukkan Salah satu parameter filter_by di atas ini",
                "parameter":field
            },status=400)

        if typeSort == 'desc':
            typeSort="-"
        else:
            typeSort=""

        # Sesuaikan dengan Django ORM
        if sortParam == 'username':
            sortParam = 'user__username'
        elif sortParam == 'email':
            sortParam = 'user__email'
        elif sortParam == 'date_joined':
            sortParam = 'user__date_joined'

        if filterParam == 'username':
            filterParam=Q(user__username__icontains=filterValue)
        elif filterParam == 'email':
            filterParam=Q(user__email__icontains=filterValue)
        elif filterParam == 'date_joined':
            filterParam=Q(user__date_joined__range=filterValue)
        elif filterParam == 'city':
            filterParam=Q(city__icontains=filterValue)
        elif filterParam == 'zipcode':
            filterParam=Q(zipcode__icontains=filterValue)
        else:
            filterParam=Q()

        users=UserExtend.objects.select_related('user').filter(
            filterParam
        ).values(
            'user__username',
            'user__email',
            'user__date_joined',
            'city',
            'zipcode',
            'user_id'
        ).order_by(typeSort+sortParam)
        for user in users:
            user["username"]=user.pop("user__username")
            user["email"]=user.pop("user__email")
            user["date_joined"]=user.pop("user__date_joined")
        return Response({
            'data':users
        })