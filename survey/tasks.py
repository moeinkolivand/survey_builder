from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from celery.utils.log import get_task_logger
from survey.models import Survey

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    # TODO:: We Can Use Bulk Update!
    Survey.objects.filter(created_at__lte=one_hour_ago, is_archive=False).update(is_archive=False)
