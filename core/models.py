from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('OWNER','Owner'),
        ('TENANT','Tenant'),
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Society(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
    

class Flat(models.Model):
    flat_number = models.CharField(max_length=10)

    owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'role': 'OWNER'}
)

    tenant = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        related_name='rented_flats',
        on_delete=models.SET_NULL,
        limit_choices_to={'role':'TENANT'}
    )
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    def __str__(self):
        return self.flat_number


class MaintenenceBill(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flat.flat_number} - {self.month}"
    
class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    move_in_date = models.DateField()

    def __str__(self):
        return self.user.email



