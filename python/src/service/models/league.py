from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from python.src.data.models.league import League as LeagueStore


class League(SQLAlchemyAutoSchema):
    class Meta:
        model = LeagueStore
        include_relationships = True
        load_instance = True
        include_fk = True
