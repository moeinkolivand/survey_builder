from enum import Enum


class QuestionTypes(Enum):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'
    RATING = 'rating'
    CONTACT_INFORMATION = 'contact_information'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
