
# --- FILE: services/schema_validator.py ---
from marshmallow import Schema, fields, ValidationError

class HouseInputSchema(Schema):
    GrLivArea = fields.Float(required=True)
    TotalBsmtSF = fields.Float(required=True)
    YearBuilt = fields.Int(required=True)
    FullBath = fields.Int(required=True)
    GarageCars = fields.Int(required=True)
    OverallQual = fields.Int(required=True)

def validate_input(data):
    schema = HouseInputSchema()
    return schema.load(data)
