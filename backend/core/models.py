from django.db import models
from django.contrib.auth.models import User

class EcoAction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='eco_actions')
    action_type=models.CharField(max_length=30,default='other'); title=models.CharField(max_length=140); quantity=models.DecimalField(max_digits=10,decimal_places=2,default=1); unit=models.CharField(max_length=30,blank=True); notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
class EnvironmentalReport(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reports'); title=models.CharField(max_length=140); category=models.CharField(max_length=40,default='other'); description=models.TextField(); location_text=models.CharField(max_length=200,blank=True); status=models.CharField(max_length=20,default='submitted'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
class Challenge(models.Model):
    title=models.CharField(max_length=120); description=models.TextField(); points=models.PositiveIntegerField(default=10); duration_days=models.PositiveIntegerField(default=7); active=models.BooleanField(default=True)
class ChallengeProgress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='challenge_progress'); challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE); joined_at=models.DateTimeField(auto_now_add=True); completed_at=models.DateTimeField(null=True,blank=True)
    class Meta: unique_together=('user','challenge')
class MaterialListing(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='material_listings'); title=models.CharField(max_length=140); material_type=models.CharField(max_length=80); weight_kg=models.DecimalField(max_digits=10,decimal_places=2); description=models.TextField(blank=True); condition=models.CharField(max_length=40,default='Reusable'); pickup_location=models.CharField(max_length=200); destination_location=models.CharField(max_length=200); distance_km=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True); estimated_cost=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True); status=models.CharField(max_length=20,default='available'); delivery_proof=models.ImageField(upload_to='delivery_proofs/',null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
