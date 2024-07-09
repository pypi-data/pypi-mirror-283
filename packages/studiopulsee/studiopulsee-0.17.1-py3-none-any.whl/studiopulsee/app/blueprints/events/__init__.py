from flask import Blueprint
from studiopulsee.app.utils.api import configure_api_from_blueprint

from studiopulsee.app.blueprints.events.resources import (
    EventsResource,
    LoginLogsResource,
)

routes = [
    ("/data/events/last", EventsResource),
    ("/data/events/login-logs/last", LoginLogsResource),
]

blueprint = Blueprint("events", "events")
api = configure_api_from_blueprint(blueprint, routes)
