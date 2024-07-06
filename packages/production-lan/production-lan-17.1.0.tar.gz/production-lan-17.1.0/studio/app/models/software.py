from studio.app import db
from studio.app.models.serializer import SerializerMixin
from studio.app.models.base import BaseMixin

from sqlalchemy.dialects.postgresql import JSONB


class Software(db.Model, BaseMixin, SerializerMixin):
    """
    Describes software used by working files.
    """

    name = db.Column(db.String(40), unique=True, nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    file_extension = db.Column(db.String(20), nullable=False)
    secondary_extensions = db.Column(JSONB)
