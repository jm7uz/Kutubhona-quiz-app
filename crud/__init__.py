# app/crud/__init__.py

from .region import *
from .quiz_attempt import *
from .quiz import *
from .user import *
from .question import *
from .answer import *
from .user_answer import *
from .district import *
from .organization import *

__all__ = [
    "get_regions",
    "get_region",
    "create_region",
    "update_region",
    "delete_region",
    "get_districts",
    "get_district",
    "get_districts_by_region",
    "create_district",
    "update_district",
    "delete_district",
    "get_organizations",
    "get_organization",
    "get_organizations_by_region",
    "get_organizations_by_region_and_type",
    "create_organization",
    "update_organization",
    "delete_organization",
    "get_users",
    "get_user",
    "get_user_by_username",
    "create_user",
    "update_user",
    "delete_user",
    "authenticate_user",
    "get_quizzes",
    "get_quiz",
    "create_quiz",
    "update_quiz",
    "delete_quiz",
    "get_questions",
    "get_question",
    "create_question",
    "update_question",
    "delete_question",
    "get_answers",
    "get_answer",
    "create_answer",
    "update_answer",
    "delete_answer",
    "get_quiz_attempts",
    "get_quiz_attempt",
    "create_quiz_attempt",
    "delete_quiz_attempt",
    "get_user_answers",
    "get_user_answer",
    "create_user_answer",
    "update_user_answer",
    "delete_user_answer",
]
