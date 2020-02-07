from rest_framework import serializers
from .models import Person, Email, Phone, Address


class EmailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Email
        fields = ('id', 'address')


class PhoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Phone
        fields = ('id', 'number')


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = ('id', 'address_line_1', 'address_line_2', 'address_line_3', 'country', 'state', 'city', 'postal_code')


class PersonSerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True)
    phones = PhoneSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'birth', 'emails', 'phones', 'addresses')

    def create(self, validated_data):
        emails = validated_data.pop('emails')
        phones = validated_data.pop('phones')
        addresses = validated_data.pop('addresses')
        p = Person.objects.create(**validated_data)

        for email in emails:
            Email(**email, person=p).save()
        
        for phone in phones:
            Phone(**phone, person=p).save()
        
        for address in addresses:
            Address(**address, person=p).save()

        return p
    
    def update(self, instance, validated_data):
        emails = validated_data.pop('emails')

        emails_to_delete = [email['id'] for email in emails]
        # Delete emails that are not present in the object
        instance.emails.all().exclude(id__in=emails_to_delete).delete()

        for email in emails:
            try:
                e = Email.objects.get(id=email['id'])
                e.address = email['address']
                e.save()
            except Email.DoesNotExist:
                Email(address=email['address'], person=instance).save()
        

        phones = validated_data.pop('phones')
        addresses = validated_data.pop('addresses')

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth = validated_data.get('birth', instance.birth)
        instance.save()

        return instance