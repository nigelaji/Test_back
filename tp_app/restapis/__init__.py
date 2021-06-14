from flask import Blueprint

restful_blue = Blueprint('restful', __name__)

from . import article
from . import user

