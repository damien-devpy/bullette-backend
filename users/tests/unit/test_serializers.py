import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.serializers import CreateOrUpdateUserSerializer


class TestUserRegistrationSerializer(TestCase):

    def setUp(self):
        self.data = {"username": "username",
                     "email": "test@mail.com",
                     "password": "p4ssw0rd_",
                     "password2": "p4ssw0rd_",
                     }

    def test_serializer_given_different_password_raise_validation_error(self):
        self.data['password2'] = 'a_different_password'
        serializer = CreateOrUpdateUserSerializer(data=self.data)

        with pytest.raises(serializers.ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'Les deux mots de passe ne correspondent pas' in str(err.value)

    def test_serializer_given_too_common_password_raise_validation_error(self):
        self.data['password'], self.data['password2'] = 'password', 'password'
        serializer = CreateOrUpdateUserSerializer(data=self.data)

        with pytest.raises(serializers.ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'Ce mot de passe est trop courant' in str(err.value)

    def test_serializer_effectively_hash_password(self):
        serializer = CreateOrUpdateUserSerializer(data=self.data)
        serializer.is_valid()
        new_user = serializer.save()

        assert check_password(self.data['password'], new_user.password)


class TestUpdateUserSerializer(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = get_user_model().objects.first()
        self.data = CreateOrUpdateUserSerializer(self.user).data

        (self.data['password'],
         self.data['password2']) = 'a_new_password', 'a_new_password'

    def test_update_password_successfully(self):
        serializer = CreateOrUpdateUserSerializer(self.user, self.data)
        serializer.is_valid()
        update_user = serializer.save()

        assert check_password(self.data['password'], update_user.password)

    def test_update_other_user_information_successfully(self):
        self.data['username'] = 'a_new_username'

        serializer = CreateOrUpdateUserSerializer(self.user, self.data)
        serializer.is_valid()
        update_user = serializer.save()

        assert update_user.username == self.data['username']

    def test_user_cannot_update_to_an_email_that_already_exist(self):
        self.data['email'] = 'username2@mail.com' # Existing email

        serializer = CreateOrUpdateUserSerializer(self.user, self.data)

        with pytest.raises(ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'ce champ Adresse électronique existe déjà' in str(err)
