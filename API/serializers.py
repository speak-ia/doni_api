from rest_framework import serializers
from .models import Organisation, Admin, Enquete, Enqueteur, EnqueteAssignment


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'email', 'name', 'organisation']


class EnqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquete
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'organisation', 
            'status', 'required_localisation', 'min_experience', 'skills', 
            'max_enqueteurs', 'remuneration', 'additional_instructions', 
            'published', 'created_by'
        ]
        read_only_fields = ['published', 'created_by']


class EnqueteAssignmentSerializer(serializers.ModelSerializer):
    enqueteur = serializers.StringRelatedField(read_only=True)
    enquete = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EnqueteAssignment
        fields = ['id', 'enqueteur', 'enquete', 'application_status', 'assigned_date']


class EnqueteurSerializer(serializers.ModelSerializer):
    applied_enquetes = EnqueteSerializer(many=True, read_only=True)

    class Meta:
        model = Enqueteur
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number', 
            'localisation', 'date_registered', 'applied_enquetes'
        ]
