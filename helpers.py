import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
import gunicorn
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# def ResoWeb(Resoweb):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         server_token = os.environ.get("X1-ZWz1iprtc8t4p7_5xiff")
#         url = f"https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/{resource}?access_token={server_token}"
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
