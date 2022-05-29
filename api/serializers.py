from datetime import date
import email
from rest_framework import serializers
from .models import Customer
import pycountry
from .helper import valid_number
from datetime import datetime
import re
from PIL import Image


class CustomerSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(required=False, use_url=True)
    gender = serializers.CharField(max_length=10)
    class Meta:
        model = Customer

        fields = ['id', 'first_name', 'last_name', 'country_code', 'phone_number', 'gender', 'birthdate', 'avatar', 'email']
    

    # Custom validator fields
    def validate_first_name(self, first_name: str) -> list:
        if not first_name:
            raise serializers.ValidationError([{'erorr' : 'blank'}])
        return first_name


    def validate_last_name(self, last_name: str) -> list:
        if not last_name:
            raise serializers.ValidationError([{'erorr' : 'blank'}])
        return last_name


    def validate_country_code(self, country_code: str) -> list:
        if not pycountry.countries.get(alpha_2 = country_code.upper()):
            raise serializers.ValidationError([{'erorr' : 'inclusion'}])
        # Return name of country    
        return pycountry.countries.get(alpha_2 = country_code.upper()).name


    def validate_phone_number(self, phone_number: str) -> list:
        if valid_number(phone_number):
            error = valid_number(phone_number)
            list_error = []
            for i in range(len(error)):
                if error[i].isnumeric():
                    list_error.remove({'erorr' : error[i-1]})
                    list_error.append({'erorr' : error[i-1] ,'count' : int(error[i])})
                else:
                    list_error.append({'erorr' : error[i]})
            raise serializers.ValidationError(list_error)
            
        return phone_number
    
    
    def validate_gender(self, gender: str) -> list:
        if gender not in ['Male', 'male', 'Female', 'female', 'Other', 'other']:
            raise serializers.ValidationError([{'erorr' : 'inclusion'}])
        return gender
    
    def validate_birthdate(self, birthdate: date) -> list:
        if not birthdate:
            raise serializers.ValidationError([{'erorr' : 'blank'}])
        elif birthdate > datetime.date(datetime.now()):
            raise serializers.ValidationError([{'erorr' : 'in_the_future'}])
        return birthdate

    def validate_avatar(self, avatar: str) -> list:
        img = Image.open(avatar)

        if not avatar:
            raise serializers.ValidationError([{'erorr' : 'blank'}])
        elif not Image.open(avatar):
            raise serializers.ValidationError([{'erorr' : 'invalid_content_type'}])
        return avatar

    def validate_email(self, email: email) -> list:
        if Customer.objects.all().filter(email = email):
            raise serializers.ValidationError([{'erorr' : 'taken'}])
        elif not re.search(".*@.*", email):
            raise serializers.ValidationError([{'erorr' : 'invalid'}])
        return email



