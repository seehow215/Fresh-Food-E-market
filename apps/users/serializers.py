import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        validate mobile no.
        :param mobile:
        :return:
        """

        # is mobile code registered
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("User already existed.")

        # is mobile code legal
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("Illegal mobile number.")

        # frequency check
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError("Less than 60sec from last sms.")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    User Detail Serializer
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="captcha",
                                 error_messages={
                                     "blank": "Please enter code",
                                     "required": "Please enter code",
                                     "max_length": "Incorrect format",
                                     "min_length": "Incorrect format"
                                 },
                                 help_text="验证码")

    username = serializers.CharField(label="username", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="User existed.")])

    password = serializers.CharField(label="password", help_text="密码", write_only=True,
                                     style={'input_type': 'password'})

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_minute_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError("Outdated code.")

            if last_record.code != code:
                raise serializers.ValidationError("Incorrect code.")
        else:
            raise serializers.ValidationError("Incorrect code.")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
