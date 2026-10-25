from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import register,login,me,EcoActionViewSet,ReportViewSet,ChallengeViewSet,MaterialViewSet,challenge_action,dashboard,waste_classify,advisor
router=DefaultRouter(); router.register('actions',EcoActionViewSet,basename='actions'); router.register('reports',ReportViewSet,basename='reports'); router.register('challenges',ChallengeViewSet,basename='challenges'); router.register('materials',MaterialViewSet,basename='materials')
urlpatterns=[path('register/',register),path('login/',login),path('me/',me),path('dashboard/',dashboard),path('challenges/<int:pk>/<str:action>/',challenge_action),path('waste-classify/',waste_classify),path('advisor/',advisor),path('',include(router.urls))]
