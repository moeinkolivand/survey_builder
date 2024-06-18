from typing import Type
from rest_framework import serializers
from survey.enums import QuestionTypes
from survey.models import Survey, Question, Answer


class RateCreateSerializer(serializers.Serializer):
    max_rate = serializers.IntegerField(required=True)


class TextCreateSerializer(serializers.Serializer):
    text = serializers.CharField()


class ChoiceCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
    order = serializers.IntegerField()


class ContactCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'question_type', 'order',
            'survey', 'validation_rules', 'media',
            'data'
        ]

    def validate(self, data):
        if Question.objects.filter(order=data['order'], survey=data['survey']).exists():
            raise serializers.ValidationError(
                {"order": "question with this order is already exists, updating exists order is not supported yet"})
        if data.get("data", None) is not None:
            keyword_arguments = dict()
            if QuestionTypes(data['question_type']) == QuestionTypes.MULTIPLE_CHOICE:
                if data['data'].get('choices', None) is None:
                    raise serializers.ValidationError({"choices": "No choices provided"})
                keyword_arguments.update({'many': True, 'data': data['data']['choices']})
            else:
                keyword_arguments.update({'data': data['data']})
            serializer = question_create_serializer_factory(QuestionTypes(data['question_type']))(**keyword_arguments)
            serializer.is_valid(raise_exception=True)
        return data


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description']


def question_create_serializer_factory(choice_type: QuestionTypes) -> Type[serializers.Serializer]:
    if choice_type == QuestionTypes.CONTACT_INFORMATION:
        return ContactCreateSerializer
    if choice_type == QuestionTypes.MULTIPLE_CHOICE:
        return ChoiceCreateSerializer
    if choice_type == QuestionTypes.TEXT:
        return TextCreateSerializer
    if choice_type == QuestionTypes.RATING:
        return RateCreateSerializer
    raise serializers.ValidationError("invalid choice type")


class AnswerRateSerializer(serializers.Serializer):
    rate = serializers.IntegerField()


class AnswerTextSerializer(serializers.Serializer):
    text = serializers.CharField()


class AnswerChoiceSerializer(serializers.Serializer):
    choice = serializers.IntegerField()


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'user', 'user_answer', 'question')


def answer_create_serializer_factory(question_type: QuestionTypes) -> Type[serializers.Serializer]:
    if question_type == QuestionTypes.MULTIPLE_CHOICE:
        return AnswerChoiceSerializer
    if question_type == QuestionTypes.TEXT:
        return AnswerTextSerializer
    if question_type == QuestionTypes.RATING:
        return AnswerRateSerializer
    if question_type == QuestionTypes.CONTACT_INFORMATION:
        return ContactCreateSerializer
    raise serializers.ValidationError("invalid question type")
