from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets,status,filters
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from .models import EcoAction,EnvironmentalReport,Challenge,ChallengeProgress,MaterialListing
from .serializers import EcoActionSerializer,ReportSerializer,ChallengeSerializer,MaterialSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
 username=str(request.data.get('username','')).strip(); password=str(request.data.get('password','')); email=str(request.data.get('email','')).strip()
 if len(username)<3 or len(password)<8: return Response({'detail':'Username must be at least 3 characters and password at least 8 characters.'},status=400)
 if User.objects.filter(username=username).exists(): return Response({'detail':'Username already exists.'},status=400)
 user=User.objects.create_user(username=username,email=email,password=password); token,_=Token.objects.get_or_create(user=user)
 return Response({'token':token.key,'username':user.username},status=201)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
 user=authenticate(username=request.data.get('username',''),password=request.data.get('password',''))
 if not user: return Response({'detail':'Invalid username or password.'},status=400)
 token,_=Token.objects.get_or_create(user=user); return Response({'token':token.key,'username':user.username})
@api_view(['GET'])
def me(request): return Response({'id':request.user.id,'username':request.user.username,'email':request.user.email})
class OwnedViewSet(viewsets.ModelViewSet):
 def perform_create(self,serializer): serializer.save(user=self.request.user)
class EcoActionViewSet(OwnedViewSet):
 serializer_class=EcoActionSerializer
 def get_queryset(self): return EcoAction.objects.filter(user=self.request.user)
class ReportViewSet(OwnedViewSet):
 serializer_class=ReportSerializer; http_method_names=['get','post','head','options']
 def get_queryset(self): return EnvironmentalReport.objects.filter(user=self.request.user)
class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=ChallengeSerializer
 def get_queryset(self): return Challenge.objects.filter(active=True)
 def get_serializer_context(self): return {'request':self.request}
@api_view(['POST'])
def challenge_action(request,pk,action):
 challenge=get_object_or_404(Challenge,pk=pk,active=True)
 progress,created=ChallengeProgress.objects.get_or_create(user=request.user,challenge=challenge)
 if action=='join': return Response({'detail':'Challenge joined.','joined':True,'completed':bool(progress.completed_at)})
 if action=='complete':
  if not progress.completed_at: progress.completed_at=timezone.now(); progress.save(update_fields=['completed_at'])
  return Response({'detail':'Challenge completed! Points awarded once.','completed':True,'points':challenge.points})
 return Response({'detail':'Unknown action'},status=400)
class MaterialViewSet(OwnedViewSet):
 serializer_class=MaterialSerializer; parser_classes=[MultiPartParser,FormParser,JSONParser]
 def get_queryset(self): return MaterialListing.objects.filter(user=self.request.user)
 def perform_create(self,serializer): serializer.save(user=self.request.user)

from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
@api_view(['GET'])
def dashboard(request):
 return Response({'actions_count':EcoAction.objects.filter(user=request.user).count(),'reports_count':EnvironmentalReport.objects.filter(user=request.user).count(),'materials_count':MaterialListing.objects.filter(user=request.user).count(),'challenges_count':Challenge.objects.filter(active=True).count()})
@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
def waste_classify(request):
 image=request.FILES.get('image')
 if not image: return Response({'detail':'Upload an image first.'},status=400)
 if image.size>8*1024*1024: return Response({'detail':'Image must be under 8 MB.'},status=400)
 name=image.name.lower()
 categories=[(('battery','cell'),('E-waste / battery','Take to an approved battery or e-waste collection point; do not place in regular recycling.')), (('cardboard','paper','carton'),('Paper / cardboard','Keep clean and dry; follow local paper recycling rules.')), (('glass','jar','bottle'),('Glass (possible)','Empty and rinse if locally accepted; confirm local collection rules.')), (('plastic','pet','wrapper'),('Plastic (possible)','Check resin markings and local recycling acceptance; film plastic often needs a separate drop-off.')), (('food','peel','organic'),('Organic waste (possible)','Use a local compost or organic waste collection service if available.'))]
 category='Uncertain — manual check needed'; guidance='The demo classifier cannot confidently identify this image. Check your local waste authority guidance or ask a trained reviewer.'
 for keys,result in categories:
  if any(k in name for k in keys): category,guidance=result; break
 return Response({'category':category,'guidance':guidance,'note':'Demo classification based mainly on file name, not a validated computer-vision model.','filename':image.name})
@api_view(['POST'])
def advisor(request):
 q=str(request.data.get('question','')).lower()
 if any(x in q for x in ['water','leak','tap','shower']): ans='Try fixing leaks promptly, use a bucket where practical, run full laundry loads, and track approximate use. For a suspected public leak, report it to the relevant local utility.'
 elif any(x in q for x in ['waste','plastic','recycl','trash','garbage']): ans='Start by separating wet/organic waste from dry recyclables, keep paper/cardboard clean and dry, avoid wish-cycling, and verify accepted materials with your local municipal rules. Batteries and e-waste need approved collection.'
 elif any(x in q for x in ['energy','electric','power','ac','light']): ans='Switch off unused lights and devices, use efficient lighting, set cooling to a reasonable temperature, improve shade/ventilation, and compare electricity use over time.'
 elif any(x in q for x in ['travel','car','transport','commute']): ans='For suitable short trips, consider walking, cycling, public transport or carpooling. Prioritize safe routes and compare the whole journey rather than distance alone.'
 elif any(x in q for x in ['food','compost','kitchen']): ans='Plan meals, store food properly, use leftovers safely, and compost suitable scraps if a local service is available. Track what gets discarded to identify patterns.'
 else: ans='Choose one measurable change this week: reduce single-use packaging, save energy, conserve water, travel more efficiently, or reuse an item. Track the action and verify local recycling/disposal rules.'
 return Response({'answer':ans,'mode':'rule-based demo advisor','disclaimer':'For high-impact decisions, verify guidance with local authorities and trusted environmental sources.'})
