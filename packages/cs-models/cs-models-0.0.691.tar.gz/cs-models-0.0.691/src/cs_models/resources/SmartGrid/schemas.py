from marshmallow import Schema, fields
from ..SmartGridCell.schemas import SmartGridCellResourceSchema


class SmartGridResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    is_deleted = fields.Boolean(allow_none=True)
    cells = fields.Nested(
        SmartGridCellResourceSchema(exclude=("smart_grid_id",)),
        many=True,
        dump_only=True,
    )
    updated_at = fields.DateTime(dump_only=True)
