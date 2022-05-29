from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from api.models import Customer
from .serializers import CustomerSerializer

import random
import string


'''
request-> Take required fileds and option fileds 
response-> return create new object with all validator Error if found
'''
# Create Customer object
class CustomerRegist(APIView):
    parser_classes = [MultiPartParser, FormParser]
     
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


'''
request-> Take phone number 
response-> return OTP (6) numbers unique
'''
# Create OTP 
@api_view(['POST'])
def createOtp(request):
    phone = str(request.data['phone'])
    
    # Check if phone is exist
    if Customer.objects.all().filter(phone_number=phone):
        customer = Customer.objects.all().filter(phone_number=phone)[0]

    if customer.otp:
        return Response({'message' : 'Sorry This Phone Number Is Valid!!'}, status=status.HTTP_200_OK)
    else:
        otp = ''.join(random.choices(string.digits ,k=6))

        return Response(otp)


'''
request-> Take 1-phone number(from cache) 2-old_otp(from cache) 3-otp(from user)
response-> return message and save otp in model
'''
# Check OTP
@api_view(['POST'])
def acceptOtp(request):
    # User Enter 
    otp = int(request.data['otp'])
    # Come From Cash
    phone = str(request.data['phone'])
    old_otp = int(request.data['old_otp'])
    # Get Customer User
    customer = Customer.objects.get(phone_number=phone)

    if old_otp == otp:
        # Save otp in model
        customer.otp = otp
        customer.save()
        return Response({'message' : 'Congrats This Phone Number Is Valid'}, status=status.HTTP_200_OK)
    else:
        return Response({'error' : 'Sorry This Phone Number Is Not Valid!! Try again'}, status=status.HTTP_400_BAD_REQUEST)


'''
request-> Take 1-phone number 2-password 3-re-password
response-> check valid data, Genrate username, create user From User Model and linked to Customer Model and return genrate auth-token   
'''
# Create OTP 
@api_view(['POST'])
def createPassword(request):
    phone = str(request.data['phone'])
    password = request.data['password']
    re_password = request.data['re_password']

    # Check if phone is exist
    if Customer.objects.all().filter(phone_number=phone):
        customer = Customer.objects.all().filter(phone_number=phone)[0]
    else:
        return Response({'error' : 'This Phone Number Is Not exist!'}, status=status.HTTP_400_BAD_REQUEST)

    # If phone has otp
    if not customer.otp:
        return Response({'error' : 'Sorry This Phone Number Is Not Valid!! Try again'}, status=status.HTTP_400_BAD_REQUEST)
    # Check From Password
    if password == re_password:
        #Genrate Username
        user_name = customer.first_name + '_' + customer.phone_number[-4:]

        # Create user Object
        user = User.objects.create_user(username=user_name, password=password)
        customer.user = user
        customer.save()

        # In Here I want to return uniqe auth-token
        token = Token.objects.create(user=customer.user)
        return Response({"Token" : token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error' : 'The password & re_password is not matching'}, status=status.HTTP_400_BAD_REQUEST)



'''
request-> Take 1-Token 2-phone number
response-> get user, customer and check if linked withsome and return Customer Serializer
'''
# Get Current User That have token 
@api_view(['POST'])
def getCustomerUser(request):
    phone = str(request.data['phone'])
    token = request.data['token']

    # Get User
    if Token.objects.all().filter(key=token):
        user = Token.objects.get(key=token).user
    else:
        return Response({'error' : 'Opps Token Is not valid!'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if phone is exist
    if Customer.objects.all().filter(phone_number=phone):
        customer = Customer.objects.all().filter(phone_number=phone)[0]
    else:
        return Response({'error' : 'This Phone Number Is Not exist!'}, status=status.HTTP_400_BAD_REQUEST)
    # Check if token for this user phone number
    if customer.user == user:
        serlizer = CustomerSerializer(customer, many=False)
        return Response(serlizer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error' : 'Oops this token not for this user!'}, status=status.HTTP_400_BAD_REQUEST)

    





