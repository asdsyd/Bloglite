from flask import render_template, request, Blueprint
from bloglite.models import Post
from flask_login import login_required


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts)

@main.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@main.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


