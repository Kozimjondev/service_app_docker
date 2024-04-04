from rest_framework import serializers

from service.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.username')
    client_company = serializers.CharField(source='client.company')
    client_email = serializers.CharField(source='client.user.email')
    plan = PlanSerializer()
    service = serializers.CharField(source='service.name')
    price = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'client_name',
            'client_company',
            'client_email',
            'service',
            'price',
            'plan',
        )

    # def get_price(self, obj):
    #     return obj.service.full_price - obj.service.full_price * obj.plan.discount / 100

    def get_price(self, obj):
        return obj.price
