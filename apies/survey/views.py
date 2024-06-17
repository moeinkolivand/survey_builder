from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from apies.survey.serializers import SurveySerializer, QuestionSerializer, answer_create_serializer_factory, \
    AnswerSerializer
from survey.enums import QuestionTypes
from survey.models import Survey, Question, Answer
from utils.pagination import CustomPageNumberPagination


class ListCreateSurveyApiView(ListCreateAPIView):
    queryset = Survey.objects.select_related("question").all()
    serializer_class = SurveySerializer
    pagination_class = CustomPageNumberPagination
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JWTAuthentication,)


class ListCreateQuestionApiView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # permission_classes = (IsAuthenticated, EditPermission)
    # authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        survey = get_object_or_404(Survey, pk=self.request.query_params.get('survey', None))
        return Question.objects.filter(survey=survey)


class AnswerApiView(ListCreateAPIView):
    serializer_class = AnswerSerializer
    pagination_class = CustomPageNumberPagination

    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Answer.objects.select_related("question").filter(question__survey__id=self.kwargs['survey_id'],
                                                                user=self.kwargs['user_id'])

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=kwargs.get('survey_id', None))
        if kwargs.get("user_id", None) is None:
            raise ValidationError({"user_id": "Please provide user_id"})
        if request.data.get('answers', None) is None or not isinstance(request.data.get('answers', None), list):
            return Response({'error': 'Answers cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        answer_data = []
        if Answer.objects.filter(question__survey=survey, user=kwargs['user_id']).exists():
            raise ValidationError({'error': 'you already answered this question'})
        if len(request.data.get('answers', None)) != Question.objects.filter(survey=survey).count():
            raise ValidationError({'error': 'Answers Not Send Completely'})
        for data in request.data['answers']:
            question = get_object_or_404(Question, pk=data.get('question', None))
            serializer = answer_create_serializer_factory(QuestionTypes(question.question_type))
            serializer(data=data).is_valid(raise_exception=True)
            answer_data.append(
                Answer(question=question, user_answer=data, user=kwargs['user_id']))
        Answer.objects.bulk_create(answer_data)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
