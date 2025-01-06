from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class AppUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_enqueteur = models.BooleanField(default=False)

    def __str__(self):
        return self.username




class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=100, choices=[
            ("ONG", "ONG"),
            ("Entreprise", "Entreprise"),
            ("Autres", "Autres"),
        ],
        default="ONG",)  
    localisation = models.CharField(max_length=255, blank=True, null=True)  
    date_inscription = models.DateField(default=now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Admin(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey(
        "API.Organisation",  
        on_delete=models.CASCADE,
        related_name="admins",
        null=True,
    )

    def __str__(self):
        return f"Admin: {self.name}"



# Investigators/Enquêteurs who apply via a mobile app
class Enqueteur(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, default="donidata@gmail.com")
    phone_number = models.CharField(max_length=20, default="70202070")
    localisation = models.CharField(max_length=255, null=True, blank=True)
    date_registered = models.DateTimeField(default=now)

    def __str__(self):
        return f"Enqueteur: {self.first_name} {self.last_name}"


# Enquete model
class Enquete(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True)  
    start_date = models.DateField()  
    end_date = models.DateField()  
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    organisation = models.ForeignKey(
        "API.Organisation",  
        on_delete=models.CASCADE,
        related_name="enquetes",
    )
    created_by = models.ForeignKey(
        "API.Admin",  
        on_delete=models.CASCADE,
        related_name="created_enquetes",
        default=0,
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
        "API.Enqueteur",  
        related_name="applied_enquetes",
        through="API.EnqueteAssignment",  
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
    assigned_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.enqueteur} -> {self.enquete}"
