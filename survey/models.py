from survey.enums import QuestionTypes
from utils.base_time_model import BaseTimeModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import HStoreField

User = get_user_model()


class Survey(BaseTimeModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"), blank=True)
    is_archive = models.BooleanField(verbose_name=_("is archive"), default=False)

    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # answered_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
        db_table = 'survey'


class Question(BaseTimeModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"))
    text = models.CharField(max_length=255, verbose_name=_("text"))
    question_type = models.CharField(max_length=20, choices=QuestionTypes.choices(), verbose_name=_("question_type"))
    order = models.IntegerField(verbose_name=_("order"))
    validation_rules = models.JSONField(default=dict, blank=True,
                                        verbose_name=_("validations"))  # Store validation rules as JSON
    data = models.JSONField(verbose_name=_("question data"), blank=True, default=dict)
    media = models.ImageField(blank=True, upload_to='question_media/',
                              verbose_name=_("media"))  # Optional media background

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'
        db_table = 'question'


class Answer(BaseTimeModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))
    user = models.IntegerField(default=1)
    user_answer = models.JSONField(verbose_name=_("user answer"), default=dict)

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = 'answers'
        verbose_name_plural = 'answers'
        db_table = 'answer'
