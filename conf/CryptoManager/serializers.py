from rest_framework import serializers

class UserContractAddressSerializer(serializers.Serializer):
    user_address = serializers.CharField(required=True)
    contract_address = serializers.CharField(required=True)
    reviewer_address = serializers.CharField(required=False)
    data = serializers.CharField(required=False)
    pdf_link = serializers.URLField(required=False)