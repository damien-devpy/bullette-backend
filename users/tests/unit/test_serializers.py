import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users.serializers import UserSerializer


class TestUserRegistrationSerializer(TestCase):

    def setUp(self):
        self.data = {"username": "username",
                     "email": "test@mail.com",
                     "password": "p4ssw0rd_",
                     "password2": "p4ssw0rd_",
                     }

    def test_serializer_given_different_password_raise_validation_error(self):
        self.data['password2'] = 'a_different_password'
        serializer = UserSerializer(data=self.data)

        with pytest.raises(serializers.ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'Les deux mots de passe ne correspondent pas' in str(err.value)

    def test_serializer_given_too_common_password_raise_validation_error(self):
        self.data['password'], self.data['password2'] = 'password', 'password'
        serializer = UserSerializer(data=self.data)

        with pytest.raises(serializers.ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'Ce mot de passe est trop courant' in str(err.value)

    def test_serializer_effectively_hash_password(self):
        serializer = UserSerializer(data=self.data)
        serializer.is_valid()
        new_user = serializer.save()

        assert check_password(self.data['password'], new_user.password)


class TestUpdateUserSerializer(TestCase):

    def setUp(self):
        existing_user = {'username': 'existing_username',
                         'email': 'existing@mail.com',
                         'password': 'password_'
                        }

        get_user_model().objects.create_user(**existing_user)

        self.data = {"username": "username",
                     "email": "test@mail.com",
                     "password": "p4ssw0rd_",
                     "password2": "p4ssw0rd_",
                     }

        serializer = UserSerializer(data=self.data)
        serializer.is_valid()
        self.new_user = serializer.save()

    def test_update_password_successfully(self):
        self.data['password'], self.data['password2'] = "a_new_password", "a_new_password"
        serializer = UserSerializer(self.new_user, self.data)
        serializer.is_valid()
        update_user = serializer.save()

        assert check_password(self.data['password'], update_user.password)

    def test_update_other_user_information_successfully(self):
        self.data['username'] = 'new_username'
        serializer = UserSerializer(self.new_user, self.data)
        serializer.is_valid()
        update_user = serializer.save()

        assert update_user.username == self.data['username']

    def test_user_cannot_update_to_an_email_that_already_exist(self):
        self.data['email'] = 'existing@mail.com'
        serializer = UserSerializer(self.new_user, self.data)

        with pytest.raises(ValidationError) as err:
            serializer.is_valid(raise_exception=True)

        assert 'ce champ Adresse électronique existe déjà' in str(err)
