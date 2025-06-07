from rest_framework import serializers

# Taking
class LoginSerializer(serializers.Serializer):  # similar to form
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        fields = '__all__'

# Returning
class TokenSerializers(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        fields = '__all__'
