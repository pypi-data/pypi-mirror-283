from studio.app.models.status_automation import StatusAutomation
from studio.app.utils import cache, fields
from studio.app.services import base_service
from studio.app.services.exception import StatusAutomationNotFoundException


def clear_status_automation_cache():
    cache.cache.delete_memoized(get_status_automations)


@cache.memoize_function(120)
def get_status_automations():
    return fields.serialize_models(StatusAutomation.get_all())


def get_status_automation_raw(status_automation_id):
    """
    Get status automation matching given id as an active record.
    """
    return base_service.get_instance(
        StatusAutomation,
        status_automation_id,
        StatusAutomationNotFoundException,
    )
