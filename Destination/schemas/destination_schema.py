from marshmallow import Schema, fields, validate

class DestinationSchema(Schema):
    # Name of the destination
    name = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Description of the destination
    description = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Location of the destination
    location = fields.Str(required=True, validate=validate.Length(min=1))
