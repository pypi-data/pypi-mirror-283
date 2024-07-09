from sqlalchemy.dialects.postgresql import JSONB

from prodt_lan.app import db
from prodt_lan.app.models.serializer import SerializerMixin
from prodt_lan.app.models.base import BaseMixin


class DataImportError(db.Model, BaseMixin, SerializerMixin):
    """
    Table to allow the storage of import errors.
    """

    event_data = db.Column(JSONB, nullable=False)
    source = db.Column(db.Enum("csv", "shotgun", name="import_source_enum"))
