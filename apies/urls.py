from django.urls import path, include

urlpatterns = [
    path('v1/survey/', include('apies.survey.urls')),
]
