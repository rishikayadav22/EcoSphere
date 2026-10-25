from django.core.management.base import BaseCommand
from core.models import Challenge
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  data=[('Carry a reusable bottle','Use a refillable bottle instead of single-use plastic.',10,1),('Low-waste day','Avoid unnecessary single-use packaging today.',20,1),('Save water','Choose one practical water-saving action each day this week.',30,7),('Walk or cycle','Replace one short vehicle trip with walking or cycling if safe.',25,1)]
  for title,description,points,days in data: Challenge.objects.get_or_create(title=title,defaults={'description':description,'points':points,'duration_days':days})
  self.stdout.write(self.style.SUCCESS('Demo challenges ready.'))
