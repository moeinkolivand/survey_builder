from rest_framework import status
from rest_framework.test import APITestCase

from survey.enums import QuestionTypes
from survey.models import Survey, Question


class SurveyApiTestCase(APITestCase):

    def test_create_survey(self):
        data = {"title": "Test survey"}
        client = self.client.post('/api/v1/survey/', data, format='json')
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(client.data['title'], data['title'])
        self.assertEqual(client.data['description'], data.get('description', ""))
        self.assertEqual(Survey.objects.count(), 1)

    def test_get_survey_list(self):
        self.test_create_survey()
        client = self.client.get('/api/v1/survey/', format='json')
        self.assertEqual(client.status_code, status.HTTP_200_OK)
        self.assertEqual(client.data['count'], Survey.objects.count())


class QuestionApiTestCase(APITestCase):

    def _create_survey(self):
        data = {"title": "Test survey"}
        c = self.client.post('/api/v1/survey/', data, format='json')
        self.assertEqual(c.status_code, status.HTTP_201_CREATED)
        return Survey.objects.first()

    def _test_question_with_data(self, url, data):
        survey = self._create_survey()
        client = self.client.post(url, data, format='json')
        question = Question.objects.filter(survey=survey.id).first()
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(question.survey.id, data['survey'])
        self.assertEqual(Question.objects.filter(question_type=data['question_type']).count(), 1)
        self.assertEqual(question.question_type, data['question_type'])
        self.assertEqual(question.text, data['text'])
        if data.get('data', None) is not None:
            self.assertEqual(question.data, data['data'])

    def test_create_question_with_type_rate(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 1,
            "question_type": QuestionTypes.RATING.value,
            "text": "how do you rate my site",
            "data": {"max_rate": 10}
        }
        url = '/api/v1/survey/question?survey=1'
        self._test_question_with_data(url, data)

    def test_create_question_with_type_text(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 2,
            "question_type": QuestionTypes.TEXT.value,
            "text": "how do you rate my site",
            "data": {"text": "are you sure about that ?"}
        }
        self._test_question_with_data('/api/v1/survey/question?survey=1', data)

    def test_create_question_with_type_contact(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 3,
            "question_type": QuestionTypes.CONTACT_INFORMATION.value,
            "text": "how do you rate my site",
        }
        self._test_question_with_data('/api/v1/survey/question?survey=1', data)

    def test_create_question_with_type_multiple_choice(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 5,
            "question_type": QuestionTypes.MULTIPLE_CHOICE.value,
            "text": "how do you rate my site",
            "data": {"choices": [{"order": 1, "text": "one"}, {"order": 2, "text": "two"}]}
        }
        self._test_question_with_data('/api/v1/survey/question?survey=1', data)

    def test_question_not_be_create_with_same_order_and_survey(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 5,
            "question_type": QuestionTypes.MULTIPLE_CHOICE.value,
            "text": "how do you rate my site",
            "data": {"choices": [{"order": 1, "text": "one"}, {"order": 2, "text": "two"}]}
        }
        self._test_question_with_data('/api/v1/survey/question?survey=1', data)
        c = self.client.post('/api/v1/survey/question?survey=1', data, format='json')
        self.assertEqual(c.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_question_data_list(self):
        survey = self._create_survey()
        data = {
            "survey": survey.id,
            "order": 5,
            "question_type": QuestionTypes.MULTIPLE_CHOICE.value,
            "text": "how do you rate my site",
            "data": {"choices": [{"order": 1, "text": "one"}, {"order": 2, "text": "two"}]}
        }
        self._test_question_with_data(f'/api/v1/survey/question?survey={survey.id}', data)
        c = self.client.get(f'/api/v1/survey/question?survey={survey.id}', format='json')
        self.assertEqual(c.status_code, status.HTTP_200_OK)
        self.assertEqual(c.data['count'], 1)


class AnswerApiTestCase(APITestCase):

    def setUp(self):
        self.survey = Survey.objects.create(title="Test survey")
        self.question = Question.objects.create(**{
            "survey": self.survey,
            "order": 3,
            "question_type": QuestionTypes.CONTACT_INFORMATION.value,
            "text": "how do you rate my site",
        })
        self.input_data = {"answers": [
            {"first_name": "aaaa", "last_name": "bbbbb", "email": "asdfjlskj@gmail.com", "question": self.question.id}
        ]}

    def test_answer_not_be_create_with_wrong_survey_and_user(self):
        survey_id = Survey.objects.count()
        client = self.client.post(f'/api/v1/survey/answer/{survey_id + 1}/1', format='json')
        self.assertEqual(client.status_code, status.HTTP_404_NOT_FOUND)
        client = self.client.post(f'/api/v1/survey/answer/{survey_id}/', format='json')
        self.assertEqual(client.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_answer(self):
        survey_id = Survey.objects.first().id
        client = self.client.post(f'/api/v1/survey/answer/{survey_id}/3', self.input_data, format='json')
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

    def test_answer_must_be_equal_with_question_number(self):
        survey_id = Survey.objects.first().id
        new_data = self.input_data['answers'].append({"choice": 2, "question": 4})
        client = self.client.post(f'/api/v1/survey/answer/{survey_id}/3', new_data, format='json')
        self.assertEqual(client.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_answered_question(self):
        survey_id = Survey.objects.first().id
        client = self.client.post(f'/api/v1/survey/answer/{survey_id}/3', self.input_data, format='json')
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        client = self.client.post(f'/api/v1/survey/answer/{survey_id}/3', self.input_data, format='json')
        self.assertEqual(client.status_code, status.HTTP_400_BAD_REQUEST)