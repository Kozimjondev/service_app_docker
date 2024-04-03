from rest_framework import serializers

from service.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.username')
    client_company = serializers.CharField(source='client.company')
    client_email = serializers.CharField(source='client.user.email')

    class Meta:
        model = Subscription
        fields = (
            'client_name',
            'client_company',
            'client_email',
            'plan',
            'service',
        )
