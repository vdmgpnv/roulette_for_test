from django.urls import path

from .views import *

urlpatterns = [
    path('start/', StartRound.as_view()),
    path('roll/', RollTheRoulette.as_view()),
    path('end/', EndRound.as_view()),
    path('statistics/', RoundStatistics.as_view()),
]