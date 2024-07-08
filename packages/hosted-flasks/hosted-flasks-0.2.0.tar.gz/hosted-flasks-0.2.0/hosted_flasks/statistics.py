import logging

from datetime import datetime
import humanize

from flask.globals import request_ctx

logger = logging.getLogger(__name__)

class Tracker:
  def __init__(self, hostedflask):
    self.hostedflask = hostedflask
    self.started     = datetime.now()
    self.hits        = 0

    try:
      self.hostedflask.handler.extensions["hosted-flasks-tracker"]
      logger.warning("f📊 {self.hostedflask.name} already has tracker")
    except KeyError:
      logger.info(f"📊 setting up tracker for {self.hostedflask.name}")
      self.hostedflask.handler.extensions["hosted-flasks-tracker"] = self
      self.hostedflask.handler.before_request(self.before_request)

  @property
  def humanized_since(self):
    return humanize.naturaltime(self.started)

  def before_request(self):
    self.track_request(request_ctx.request)

  def track_request(self, request):
    if request.endpoint in self.hostedflask.track:
      analytics = {
        "hosted-flask": self.hostedflask.name,
        "args"        : request.args,
        "url"         : request.url,
        "user_agent"  : request.user_agent.string,
        "remote_addr" : request.remote_addr,
        "referrer"    : request.referrer,
        "endpoint"    : request.endpoint,
        "path"        : request.path
      }
      logger.info(f"📊 {analytics}")
      self.hits += 1

def track(hostedflask):
  Tracker(hostedflask)
  return hostedflask
