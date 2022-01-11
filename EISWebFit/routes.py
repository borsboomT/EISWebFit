"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="EIS Web Fitting",
        description="A simple and ugly web application for fitting electrochemical impedance data.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )
