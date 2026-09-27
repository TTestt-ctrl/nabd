from flask import current_app
from mixpanel import Mixpanel

_client = None


def _mixpanel():
    global _client
    if _client is None:
        _client = Mixpanel(current_app.config["MIXPANEL_TOKEN"])
    return _client


def track(distinct_id, event, properties=None):
    if not current_app.config["MIXPANEL_TOKEN"]:
        return
    _mixpanel().track(distinct_id, event, properties or {})
