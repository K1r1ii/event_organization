from event_organization.db.data_access_objects.base import BasDAO
from event_organization.db.models import User


class UserDAO(BasDAO):
    model = User