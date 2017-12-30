import logging

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from mediaide.celery import app

from mediaide_app.confirmation import account_activation_token


# @app.task
# def send_verification_email(user_id):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=user_id)
#         title = "MediAide account confirmation"
#         content = " welcome to Mediaide. below is the account activation link ./n " \
#                   "http://192.168.43.110:8000/api/confirm/" + str(
#             account_activation_token.make_token(user)) + '/' + str(user_id)
#         send_mail(
#             title,
#             content,
#             'no-reply@mediaide.com',
#             [user.email],
#             fail_silently=False,
#         )
#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)


@app.task
def send_user_enquire_email(subject,message,email):
        send_mail(subject,
                  message,
                  'no-reply@mediaide.com',
                  [email]
        )
