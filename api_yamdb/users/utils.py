import uuid

from django.core.mail import send_mail
from rest_framework import serializers

from api_yamdb.settings import EMAIL_ADMIN


def generate_confirmation_code():
    return uuid.uuid4()


def get_and_send_confirmation_code(data):
    confirmation_code = generate_confirmation_code()
    data.update(confirmation_code=confirmation_code)
    subject = 'Ваш код, для получения token.'
    message = (
        f'Ваш код для получения token: {confirmation_code}')
    send_mail(subject, message, EMAIL_ADMIN, [data[0].email])


def no_name(value):
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Использовать имя "me" в качестве username запрещено!'
        )
