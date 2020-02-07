from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth = models.DateField()

    def __str__(self):
        return "{} year of birth {}".format(self.first_name, self.birth.year)

    @property
    def emails(self):
        return self.email_set.all()

    @property
    def phones(self):
        return self.phone_set.all()

    @property
    def address(self):
        return self.address_set.all()


class Email(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="emails")
    address = models.EmailField()


class Phone(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="phones")
    number = models.CharField(max_length=125)


class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="addresses")
    address_line_1 = models.CharField(max_length=125)
    address_line_2 = models.CharField(max_length=125)
    address_line_3 = models.CharField(max_length=125)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=16)