from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'password2', 'is_citizen']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Custom validation.
        Make sure that passwords matches and syntax is sufficient secure.
        """
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError(
                'Les deux mots de passe ne correspondent pas.')

        try:
            validate_password(password=data['password'])
        except ValidationError as err:
            raise serializers.ValidationError(err)

        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get(field))
            else:
                setattr(instance, field, validated_data.get(field))
        instance.save()

        return instance
