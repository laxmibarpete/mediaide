from django.core.mail import send_mail
from rest_framework import serializers

from mediaide_app.confirmation import account_activation_token
from mediaide_app.models import CustomUser, CountriesVisa, Facilities, MedicalPackages, UserEnquiry, ContactUs, \
    UserDocuments


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'country', 'password', 'phone', 'address', 'dob', 'gender', 'confirm_password', 'agree')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        return super(CustomUserSerializer, self).update( instance,validated_data)

    def validate(self, data):
        '''
        Ensure the passwords are the same
        '''
        if not data.get('agree',False):
            raise serializers.ValidationError(
                "Please accept term and condition"
            )

        if data.has_key('password'):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError(
                    "The passwords have to be the same"
                )
            data.pop('confirm_password')

        return data


class UserDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments
        fields = ('user', 'name','description', 'document')

    def to_representation(self, value):
        response = dict(super(UserDocumentsSerializer, self).to_representation(value))
        response['document'] = "{}{}".format('api', value.document.url)
        print response['document']
        return response


class CountryVisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesVisa
        fields = ('name', 'email', 'phone', 'fax', 'website', 'embassy')


class MedicalPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPackages
        fields = ('id', 'name_of_treatment', 'no_of_days_in_hospital', 'no_of_days_out_hospital', 'approximate_cost')


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = ('name','cost')


class UserEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnquiry
        fields = ('id', 'name', 'dob', 'phone', 'gender', 'email', 'message', 'appointment_date', 'reason')

    def create(self, validate_data):
        user_enquiry = super(UserEnquirySerializer, self).create(validate_data)
        return user_enquiry



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('id', 'name','email','message','subject','phone')

    def create(self,validate_data):
        contact_us = super(ContactUsSerializer ,self).create(validate_data)
        return contact_us

