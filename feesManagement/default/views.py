from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from . serialisers import *
from . models import *
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
import random
import uuid
from django.db.models import Sum

@api_view(['GET'])
def homepage(request):
    res = {
        "computers":"/computers"
    }
    return Response(res, status=status.HTTP_200_OK)

@api_view(['GET'])
def stats_view(request, *args, **kwargs):
    users_count = User.objects.all().count()
    students_count = Students.objects.all().count()
    amount_collected = AmountPaid.objects.all().aggregate(Sum("amount"))
    response = {
        "user_count":users_count,
        "students_count":students_count,
        "amount_collected":amount_collected['amount__sum'] 
    }
    return Response(response, status=status.HTTP_200_OK)

# Create your views here.
@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(
        data = request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    created, token = AuthToken.objects.create(user)
    return Response({
        'user_info':{
            'id':user.id,
            #'username':user.username,
            'email':user.email,
            'fullname':user.get_full_name()
        },
        'token':token
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request, *args, **kwargs):
    data = request.data
    if data['id'] and data['password'] and data['old_password']:
        user = User.objects.get(id=data['id'])
        if user.check_password(data['old_password']):
            user.set_password(data['password'])
            user.save()
            msg = f"Hello {user.get_full_name()}, your password has been changed successfully!" 
        else:
            msg = "your old password is wrong!"
    else:
        msg = "please provide user id, old password and desired password"
    info = {"message":msg}
    return Response(info)

@api_view(['POST'])
def password_reset(request, *args, **kwargs):
    data = request.data
    if data['username']:
        try:
            user = User.objects.get(Q(username = data['username']) | Q(email=data['username']))
            random_no = random.randint(1000,9999)
            link = uuid.uuid4()
            PasswordResets.objects.update_or_create(
                user = user,
                code = random_no,
                link = link
            )
            msg = f"Hello {user.get_full_name()}, please check your email for link!" 
        except User.DoesNotExist:
            msg = f"no user found with username or email {data['username']}"
    else:
        msg = "please provide user id and password"
    info = {"message":msg}
    return Response(info)

@api_view(['POST'])
def password_reset_done(request, *args, **kwargs):
    data = request.data
    if data['code'] and data['password']:
        try:
            user = PasswordResets.objects.get(code = data['code'])
            user = User.objects.get(id = user.user.id)
            user.set_password(data['password'])
            user.save()
            msg = f"Hello {user.get_full_name()}, your password has been changed successfully!" 
        except PasswordResets.DoesNotExist:
            msg = f"please provide a valid code"
    else:
        msg = "please provide a code and new password"
    info = {"message":msg}
    return Response(info)


@api_view(['GET','POST'])
def user_profiles(request, *args, **kwargs):
    if request.method == "GET":
        search = request.GET.get("search")
        all_profiles = Students.objects.all()
        if search:
            all_profiles = all_profiles.filter(name__icontains = search)
        serializer = StudentsSerializer(
            all_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = request.data
        try:
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['username'],
                email = data['email']
            )
            user.set_password(data['password'])#rightly fully sets password
            user.save()
        except IntegrityError as e:
            msg = {
                "error":f"user with username {data['username']} exists",
                "additional_infomation":f"{e}"
            }
            return Response(msg)
        else:
            Students.objects.create(
                user = user,
                student_number = data['student_number'],
                dob = data['dob'],
                nationality = data['nationality'],
                gender = data['gender'],
                image = data['image']
            )
            return Response({"msg":"success register"}, 
                    status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def user_profile_detail(request, slug):
    if request.method == 'GET':
        try:
            selected_profile = UserProfile.objects.get(owner__id=slug)
        except UserProfile.DoesNotExist:
            return Response({"details":"No data found for specified id"}, status=status.HTTP_404_NOT_FOUND)
        details = {
            "full_name":selected_profile.owner.get_full_name(),
            "email":selected_profile.owner.email,
            "gender":selected_profile.gender,
            "dob":selected_profile.dob,
            "address":selected_profile.address,
            "contact":selected_profile.contact
        }
        return Response(details, status=status.HTTP_200_OK)
    else:
        data = request.data
        to_update = UserProfile.objects.get(owner = User.objects.get(id = slug))
        print(data)
        to_update.contact = data['contact']
        to_update.address = data['address']
        to_update.save()
        
        msg = {
            "msg": "update successfully"
        }
        return Response(msg, status=status.HTTP_202_ACCEPTED)
        

@api_view(['GET','POST'])
def payments(request, *args, **kwargs):
    start_date = request.GET.get("start-date")
    end_date = request.GET.get("end-date")
    search = request.GET.get("name")
    if request.method == "GET":
        if kwargs:
            slug = kwargs['slug']
            payments =AmountPaid.objects.filter(
                student__id = slug
            )
            serializer = AllPaymentsSerializer(payments, many=True)
            return Response(serializer.data)
        if start_date and end_date:
            payments =AmountPaid.objects.filter(date__range = [start_date, end_date])
            returned = []
            for x in payments:
                returned.append({
                    "id": x.id,
                    "amount": x.amount,
                    "date": x.date,
                    "name": x.student.name,
                    "level": x.level.name,
                    "student_id":x.student.id,
                    "level_id":x.level.id
                })
            return Response(returned)
        if search:
            payments =AmountPaid.objects.filter(student__name__iexact = search)
            returned = []
            for x in payments:
                returned.append({
                    "id": x.id,
                    "amount": x.amount,
                    "date": x.date,
                    "name": x.student.name,
                    "level": x.level.name,
                    "student_id":x.student.id,
                    "level_id":x.level.id
                })
            return Response(returned)
        serializer = AllPaymentsSerializer.all_students()
        return Response(serializer)
    else:
        serialiser = AllPaymentsSerializer(
            data=request.data
        )
        if serialiser.is_valid():
            serialiser.save()
            return Response({"msg":"data saved"}, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_404_NOT_FOUND)

#for one item
@api_view(['GET', 'PUT', 'DELETE'])
def payment_detail(request, slug):
    try:
        payment_effected = AmountPaid.objects.get(pk=slug)
    except AmountPaid.DoesNotExist:
        return Response({"details":"No data found for specified id"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AllPaymentsSerializer(payment_effected)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = AllPaymentsSerializer(payment_effected, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment_effected.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)