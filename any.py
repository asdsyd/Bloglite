import os
from flask import url_for

print(os.path.join(os.getcwd(), 'static/post_pics'))
print(url_for('static/post_pics'))