from mediaide_app.message import Message
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db.models import signals
from django.core.mail import send_mail
# Create your models here.
from django.utils.translation import ugettext_lazy as _

from mediaide_app.confirmation import account_activation_token
from mediaide_app.manager import UserManager
from mediaide_app.tasks import  send_user_enquire_email

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=30, blank=True)
    dob = models.DateTimeField(_('date of birth'), auto_now_add=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    country = models.CharField(_('country'), max_length=30, blank=True)

    gender = models.CharField( max_length=7, choices=GENDER_CHOICES)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    address = models.CharField(max_length=70, blank=True)
    date_joined =  models.DateTimeField(auto_now_add=True)
    agree = models.BooleanField(_('T&C'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        return self.name.strip()

    def get_short_name(self):
        """ Returns the short name for the user. """
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class TermsAndConditions(models.Model):
    description = models.TextField()


class UserDocuments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='document')
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CountriesVisa(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    phone = models.IntegerField()
    fax = models.CharField(max_length=20)
    website = models.URLField(max_length=200, null=True, blank=True)
    embassy = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}-{}".format(self.name,self.embassy)


class MedicalPackages(models.Model):
    name_of_treatment = models.CharField(max_length=255)
    no_of_days_in_hospital = models.IntegerField(default=1)
    no_of_days_out_hospital = models.IntegerField(default=0)
    approximate_cost = models.FloatField(default=0)

    def __unicode__(self):
        return self.name_of_treatment


class UserTreatmentPackages(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    treatment_package = models.ForeignKey(MedicalPackages,on_delete=models.CASCADE)

    def __unicode__(self):
        return "{}-{}".format(self.user,self.treatment_package)


class UserEnquiry(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    email = models.EmailField(_('email address'))
    message =models.TextField(null=True, blank=True)
    appointment_date = models.DateTimeField(_('appointment date'), auto_now_add=True)
    #TODO we have to make list
    reason = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.appointment_date)


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'))
    phone = models.CharField(max_length=12, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Facilities(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField()

    def __unicode__(self):
        return "{}-{}".format(self.name, self.cost)


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


def user_post_save(sender, instance, signal, *args, **kwargs):
    if kwargs.get('created'):
        title = "MediAide account confirmation"
        content = " welcome to Mediaide. below is the account activation link ./n " \
                  "http://192.168.43.110:8000/api/confirm/" + str(
            account_activation_token.make_token(instance)) + '/' + str(instance.id)

        send_user_enquire_email.delay(title, content, instance.email)
signals.post_save.connect(user_post_save, sender=CustomUser)


def user_enquire_post_save(sender, instance, signal, *args, **kwargs):
    if kwargs.get('created'):
        subject = 'Welcome to MediAide'
        message = Message
        send_user_enquire_email.delay(subject,message,instance.email)
signals.post_save.connect(user_enquire_post_save, sender=UserEnquiry)


def contact_us_post_save(sender, instance, signal, *args, **kwargs):
    if kwargs.get('created'):
        subject = 'Welcome to MediAide'
        message = Message
        send_user_enquire_email.delay(subject,message,instance.email)
signals.post_save.connect(contact_us_post_save, sender=ContactUs)
