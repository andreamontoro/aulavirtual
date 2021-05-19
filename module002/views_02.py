from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import Post, get_db, Comment
from module002.forms import PostForm, CommentForm #Error de importar por que no los lee bien.
from application import get_app

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

db = get_db()
app = get_app()

@module002.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #flash("1.1")
    form = PostForm()
    if form.validate_on_submit():
        flash("2.1")
        flash(form.body.data)

        flash(current_user.username)
        post = Post(body=form.body.data,
                    author_id=current_user.id)

        db.session.add(post)
        db.session.commit()

    flash("3.1")
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        flash("4.1")
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        flash("5.1")
        query = current_user.followed_posts
    else:
        flash("5.2")
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    flash("6.1")
    return render_template('module002_index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)






@module002.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('module002_post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@module002.route('/test')
def module002_test():
    return 'OK'
