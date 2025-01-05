from django.db import models
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    is_admin = models.BooleanField(default=False)  
    is_enqueteur = models.BooleanField(default=False) 

    def __str__(self):
        return self.username



class Organisation(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)  
    localisation = models.CharField(max_length=255)  
    date_inscription = models.DateField(auto_now_add=True)  
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="admins", null=True
    )

    def __str__(self):
        return f"Admin: {self.name}"


# Investigators/Enquêteurs who apply via a mobile app
class Enqueteur(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    localisation = models.CharField(max_length=255)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enqueteur: {self.first_name} {self.last_name}"


# Enquete model
from django.db import models
from .models import Organisation, Admin, Enqueteur

class Enquete(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=255)  # Titre de l'enquête
    description = models.TextField(blank=True, null=True)  # Description de l'enquête
    start_date = models.DateField()  # Date de début de l'enquête
    end_date = models.DateField()  # Date de fin de l'enquête
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")  # Statut de l'enquête

    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="enquetes"
    )  
    created_by = models.ForeignKey(
        Admin, on_delete=models.CASCADE, related_name="created_enquetes"
    ) 
    published = models.BooleanField(default=False)  

    required_localisation = models.CharField(
        max_length=255, blank=True, null=True
    )  
    min_experience = models.PositiveIntegerField(
        default=0
    )  
    skills = models.TextField(
        blank=True, null=True
    ) 
    max_enqueteurs = models.PositiveIntegerField(
        default=1
    ) 
    remuneration = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    ) 
    additional_instructions = models.TextField(
        blank=True, null=True
    )  
    enqueteurs = models.ManyToManyField(
        Enqueteur, related_name="applied_enquetes", through="EnqueteAssignment"
    )

    def __str__(self):
        return self.title



# Linking enquêteurs and enquetes with a status for their application
class EnqueteAssignment(models.Model):
    enqueteur = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    application_status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
    )
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enqueteur} -> {self.enquete}"
