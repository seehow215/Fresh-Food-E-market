import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from MxShop.settings import REGEX_MOBILE
from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'goods'],
                message="Already Faved"
            )
        ]

        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        # include id for ease of deletion
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    signer_name = serializers.CharField(required=True, allow_blank=False)
    signer_mobile = serializers.CharField(max_length=11)

    def validate_signer_mobile(self, signer_mobile):
        """
        validate singer mobile no.
        :param signer_mobile:
        :return:
        """
        # is mobile number legal
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("Illegal mobile number.")

        return signer_mobile

    class Meta:
        model = UserAddress

        validators = [
            UniqueTogetherValidator(
                queryset=UserAddress.objects.all(),
                fields=['user', 'province', 'city', 'district', 'address'],
                message="Address already existed."
            )
        ]

        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "id", "add_time")
