import os
import sys

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(root_path, "site-packages"))
from flask import Blueprint

# 创建登录页面蓝图
login = Blueprint('login', __name__, url_prefix='/')
# 创建主页蓝图
charts = Blueprint('admin', __name__, url_prefix='/')

from views import login
from views import data_search
