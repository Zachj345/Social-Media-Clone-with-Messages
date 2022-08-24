from .models import User, Post, Comment, Like, db
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint

views = Blueprint('views', __name__, template_folder='templates',
                  static_folder='static')


'''ROUTES'''


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@ login_required
def home():
    if request.method == 'POST':
        text = request.form.get('post')
        if text == None:
            flash('Must enter text before', category='error')
            return redirect(url_for('home'))
        if text == '' or text == ' ':
            flash('please actually post some words', category='error')
        else:
            post = Post(text=text, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('successfully added post!', category='success')

            return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user,
                           posts=sorted(Post.query.all(),
                                        key=lambda n: n.id, reverse=True),
                           user_search=User.query.all())


@views.route('/add-comment/<post_id>', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()
    postId = post.id

    if request.method == 'POST':
        comment = request.form.get('comment')
        if not comment:
            print('input not found')
            return jsonify({'error': 'No comment to add'}, 400)
        else:
            post = Post.query.filter_by(id=post_id).first()
            if post:
                print('found post')
                new_comment = Comment(text=comment,
                                      user_id=current_user.id, post_id=post_id)
                db.session.add(new_comment)
                db.session.commit()
                print([i for i in Comment.query.all()])

            else:
                flash('No post available', category='error')

    return jsonify({'success': 'facts', 'postId': postId})


@views.route('/delete-post/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        print('post not found')
        return redirect(url_for('views.home'))
    if post.comments:
        print(post.comments)
        (db.session.delete(i) for i in post.comments)
    if post.likes:
        print([i for i in post.likes])
        (db.session.delete(i) for i in post.likes)

    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return jsonify({'success': 'facts', 'postId': post_id})


@views.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return jsonify({'error': 'No comment to delete'}, 400)
    elif comment.user_id != current_user.id and comment.post.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to delete this comment'}, 400)
    else:
        db.session.delete(comment)
        db.session.commit()
        postId = comment.post_id
        post = Post.query.filter_by(id=postId).first()
        return jsonify({'success': 'facts', 'commentId': comment_id,
                        'commentLen': len(post.comments), 'postId': postId})


@views.route('/like-post/<post_id>', methods=['GET', 'POST'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes': len(post.likes),
                    'liked': current_user.id in map(lambda n: n.user_id, post.likes)})


@views.route('/del-posts/<user_id>', methods=['GET', 'POST'])
@login_required
def del_posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('no user with that id', category='error')
    elif user.posts:
        print([i for i in user.posts])
        (db.delete(i) for i in user.posts)
        db.session.commit()
        return redirect(url_for('views.home'))


@views.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User with this profile not found', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    print([i for i in posts])
    return render_template('profile.html', user=current_user, profile_user=user,
                           posts=posts, user_search=User.query.all())


name = []


@views.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == 'POST':
        search_name = request.form.get('search')
        if search_name:
            search_name = search_name.lower()
            name.append(search_name)
            print('name in post:', name[-1])
            p_user = User.query.filter_by(username=search_name).first()
            if not p_user:
                flash('User does not exist, please check your spelling',
                      category='error')
                return redirect(url_for('views.home'))
            else:
                posts = p_user.posts
                return render_template('profile.html', user=current_user, profile_user=p_user,
                                       posts=posts, user_search=User.query.all())
    print('name:', name)
    profile_user = User.query.filter_by(username=name[-1]).first()
    return render_template('profile.html', user=current_user, profile_user=profile_user,
                           posts=profile_user.posts,
                           user_search=User.query.all())
