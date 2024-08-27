#!/usr/bin/env python3
"""
A Basic Flask application with i18n and timezone support
"""
import pytz
import datetime
from typing import Dict, Union

from flask import Flask, g, request, render_template
from flask_babel import Babel, force_locale, format_datetime


class Config(object):
    """
    Application configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Instantiate the application object
app = Flask(__name__)
app.config.from_object(Config)

# Wrap the application with Babel
babel = Babel(app)

# Sample user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details
    Args:
        id (str): user id
    Returns:
        (Dict): user dictionary if id is valid else None
    """
    return users.get(int(id), None)


@app.before_request
def before_request() -> None:
    """
    Adds valid user to the global session object `g` and sets locale and timezone
    """
    user = get_user(request.args.get('login_as', 0))
    setattr(g, 'user', user)
    
    # Determine locale
    locale = request.args.get('locale', '').strip()
    if not locale and user:
        locale = user.get('locale', Config.BABEL_DEFAULT_LOCALE)
    if locale not in Config.LANGUAGES:
        locale = Config.BABEL_DEFAULT_LOCALE

    # Determine timezone
    tz = request.args.get('timezone', '').strip()
    if not tz and user:
        tz = user.get('timezone')
    try:
        tz = pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        tz = Config.BABEL_DEFAULT_TIMEZONE

    # Apply the locale and timezone
    with force_locale(locale):
        setattr(g, 'time', format_datetime(datetime.datetime.now(tz=pytz.timezone(tz))))


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic HTML template
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
