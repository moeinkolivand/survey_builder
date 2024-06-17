from django.urls import path
from apies.survey.views import ListCreateSurveyApiView, ListCreateQuestionApiView, AnswerApiView

urlpatterns = [
    path('', ListCreateSurveyApiView.as_view(), name='create survey'),
    path('question', ListCreateQuestionApiView.as_view(), name='create question'),
    path('answer/<int:survey_id>/<int:user_id>', AnswerApiView.as_view(), name='survey'),
]
