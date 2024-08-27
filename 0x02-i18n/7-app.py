#!/usr/bin/env python3
""" 2. get timezone from request """
import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """ Config class for app """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as: str) -> dict:
    """ Get user from users """
    return users.get(int(login_as), None)


@app.before_request
def before_request() -> None:
    """ Before request """
    user = get_user(request.args.get('login_as'))
    if user:
        g.user = user


@babel.localeselector
def get_locale() -> str:
    """ Get locale from request """
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user.get('locale') in app.config["LANGUAGES"]:
        return g.user.get('locale')
    header_locale = request.headers.get('locale')
    if header_locale and header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    """ get timezone from request. """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route("/")
def welcome() -> str:
    """ / page """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
