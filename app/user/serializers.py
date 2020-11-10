from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _




 

class UserSerializer(serializers.ModelSerializer):
    """serializer for thw user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # now we should make more configuration and make password at least 5 chars:
        extra_kwargs = {'password': { 'write_only': True , 'min_length': 5 }}

    def create(self, validated_data):
        """ 
        creating user with encrypted password and returninh it.
        validated_data would be everything that would come from user object as JSON format in HTTP POST. actually here would be fields of get_user_model.
        """
        return get_user_model().objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        """ update a user, setting the pasword correctly and return it."""
        password = validated_data.pop('password', None)  #pop would remove password data and will set it to None for us to replace it to new password.
        user = super().update(instance, validated_data)  # im not sure but i think super will call defaut function on itself.
        
        if password:
            user.set_password(password)
            user.save()
        
        return user


class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user authentication object."""
    email = serializers.CharField()
    password = serializers.CharField(
        style = { 'input_type': 'password'} ,
        trim_whitespace = False,
    )

    def validate(self, attrs):   # attributes are everything yhe method will get to validate the user lke email or password!
        """validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request =self.context.get('request'),
            username = email,
            password = password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials!')
            raise serializers.ValidationError(msg, code='authentication')

        # when we overwright validate function we must return values(attrs) at the end:
        attrs['user'] = user
        return attrs