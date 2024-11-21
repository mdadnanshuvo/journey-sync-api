from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role = fields.String(
        required=True, 
        validate=validate.OneOf(['Admin', 'User'], error="Role must be either 'Admin' or 'User'")
    )
