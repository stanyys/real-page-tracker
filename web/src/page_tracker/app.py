"""Flask app that counts and displays page views using Redis."""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """Increment the page view counter and return the current count."""
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")  # pylint: disable=E1101
        return "Sorry, something went wrong \N{PENSIVE FACE}", 500
    return f"This page has been seen {page_views} times."


@cache
def redis():
    """Return a cached Redis client, created once from REDIS_URL."""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
