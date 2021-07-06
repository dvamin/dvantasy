from flask import Blueprint, request
from python.src.service.utils import route_config
from python.src.service.models.league import League
from python.src.data.util.dbutil import get_league, create_league, update_league
from typing import Optional

league_bp = Blueprint("league", __name__)


@route_config({
    "blueprint": league_bp,
    "route": "/<int:league_id>",
    "methods": ["GET"],
    "response_schema": League,
    "code_on_success": 200
})
def _get_league(league_id: int) -> Optional[League]:
    return get_league(league_id)


@route_config({
    "blueprint": league_bp,
    "route": "/<int:league_id>",
    "methods": ["POST"],
    "request_schema_body": League,
    "code_on_success": 201
})
def _create_league(league_id: int) -> None:
    league: dict = request.json
    if league.id != league_id:
        raise RuntimeError("Invalid parameters specified; id's don't match")
    create_league(league["name"], league["commissioner_id"])


@route_config({
    "blueprint": league_bp,
    "route": "/<int:league_id>",
    "methods": ["PUT"],
    "request_schema": League,
    "code_on_success": 204
})
def _update_league(league_id: int) -> None:
    league = request.json
    if league.id != league_id:
        raise RuntimeError("Invalid parameters specified; id's don't match")
    update_league(league_id, league)
