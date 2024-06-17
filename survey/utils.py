from typing import Type

from survey.enums import QuestionTypes
# from survey.models import MultipleChoice, RateChoice, TextChoice, ContactInformationChoice, ChoiceAnswer, RatingAnswer
# from survey.types import ChoiceT


class ChoiceFactory:
    @staticmethod
    def get_choice_model_by_type(choice_type: QuestionTypes):
        pass
        # if choice_type == QuestionTypes.MULTIPLE_CHOICE:
        #     return MultipleChoice
        # if choice_type == QuestionTypes.RATING:
        #     return RateChoice
        # if choice_type == QuestionTypes.TEXT:
        #     return TextChoice
        # if choice_type == QuestionTypes.CONTACT_INFORMATION:
        #     return ContactInformationChoice
        # raise ValueError(f'Choice type {choice_type} not supported')

#
# class AnswerFactory:
#     @staticmethod
#     def get_answer_model_by_type(answer_type: QuestionTypes) -> Type[ChoiceT]:
#         if answer_type == QuestionTypes.MULTIPLE_CHOICE:
#             return ChoiceAnswer
#         if answer_type == QuestionTypes.RATING:
#             return RatingAnswer