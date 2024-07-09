from prodt_lan.app import db
from prodt_lan.app.models.serializer import SerializerMixin
from prodt_lan.app.models.base import BaseMixin


class Department(db.Model, BaseMixin, SerializerMixin):
    """
    Studio department like modeling, animation, etc.
    """

    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
    archived = db.Column(db.Boolean(), default=False)
