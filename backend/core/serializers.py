from rest_framework import serializers
from .models import EcoAction,EnvironmentalReport,Challenge,ChallengeProgress,MaterialListing
class EcoActionSerializer(serializers.ModelSerializer):
 class Meta: model=EcoAction; fields=['id','action_type','title','quantity','unit','notes','created_at']; read_only_fields=['id','created_at']
class ReportSerializer(serializers.ModelSerializer):
 class Meta: model=EnvironmentalReport; fields=['id','title','category','description','location_text','status','created_at']; read_only_fields=['id','status','created_at']
class ChallengeSerializer(serializers.ModelSerializer):
 joined=serializers.SerializerMethodField(); completed=serializers.SerializerMethodField()
 class Meta: model=Challenge; fields=['id','title','description','points','duration_days','active','joined','completed']
 def get_joined(self,obj): return ChallengeProgress.objects.filter(user=self.context['request'].user,challenge=obj).exists()
 def get_completed(self,obj): return ChallengeProgress.objects.filter(user=self.context['request'].user,challenge=obj,completed_at__isnull=False).exists()
class MaterialSerializer(serializers.ModelSerializer):
 class Meta: model=MaterialListing; fields=['id','title','material_type','weight_kg','description','condition','pickup_location','destination_location','distance_km','estimated_cost','status','delivery_proof','created_at']; read_only_fields=['id','user','status','delivery_proof','created_at']
