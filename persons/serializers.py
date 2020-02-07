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
                Email(**email, person=instance).save()
        

        phones = validated_data.pop('phones')
        phones_to_delete = [phone['id'] for phone in phones]
        # Delete phones that are not present in the object
        instance.phones.all().exclude(id__in=phones_to_delete).delete()

        for phone in phones:
            try:
                p = Phone.objects.get(id=phone['id'])
                p.number = phone['number']
                p.save()
            except Phone.DoesNotExist:
                Phone(**phone, person=instance).save()
        
        addresses = validated_data.pop('addresses')
        addresses_to_delete = [address['id'] for address in addresses]
        # Delete addresses that are not present in the object
        instance.addresses.all().exclude(id__in=addresses_to_delete).delete()

        for address in addresses:
            try:
                a = Address.objects.get(id=address['id'])
                a.address_line_1 = address['address_line_1']
                a.address_line_2 = address['address_line_2']
                a.address_line_3 = address['address_line_3']
                a.country = address['country']
                a.state = address['state']
                a.city = address['city']
                a.postal_code = address['postal_code']
                a.save()
            except Address.DoesNotExist:
                Address(**address, person=instance).save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth = validated_data.get('birth', instance.birth)
        instance.save()

        return instance