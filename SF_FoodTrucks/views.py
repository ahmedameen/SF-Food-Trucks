"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import current_app, Blueprint

viewsBP = Blueprint('views', __name__)


@viewsBP.route('/')
@viewsBP.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
    )


@viewsBP.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html')


@viewsBP.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
