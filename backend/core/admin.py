from django.contrib import admin
from .models import EcoAction,EnvironmentalReport,Challenge,ChallengeProgress,MaterialListing
admin.site.register([EcoAction,EnvironmentalReport,Challenge,ChallengeProgress,MaterialListing])
