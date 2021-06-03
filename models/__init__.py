import os
import sys

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(root_path, "site-packages"))
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()