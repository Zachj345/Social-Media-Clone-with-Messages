from flask import render_template, request, jsonify
from flask_login import current_user, login_required
from flask_socketio import send, SocketIO, emit
from website.views import views
from website.auth import auth
from website.models import User, Chat, Messages, app, db


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


socketio = SocketIO(app, cors_allowed_origins='*')


'''MESSAGES FUNCTIONALITY'''


@app.route('/unsend-chat-message/<message_id>', methods=['GET', 'POST'])
def unsend_message(message_id):
    message = Chat.query.filter_by(id=message_id).first()
    if not message:
        return jsonify({'error': 'No message to delete'}, 400)
    elif message.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to delete this message'}, 400)
    else:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'success': 'facts', 'messageId': message_id})


@app.route('/unsend-message/<message_id>', methods=['GET', 'POST'])
def unsend_dm(message_id):
    message = Messages.query.filter_by(id=message_id).first()
    if not message:
        return jsonify({'error': 'No message to delete'}, 400)
    elif message.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to delete this message'}, 400)
    else:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'success': 'facts', 'messageId': message_id})


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    convos = [i for i in Messages.query.all()
              if i.sender == current_user.username or i.receiver == current_user.username]
    messages = sorted(convos, key=lambda n: n.id, reverse=True)

    users_spoken_to = list(set([i.sender for i in messages] +
                               [i.receiver for i in messages]))
    current_name = current_user.username

    convo_keys = sorted([User.query.filter_by(username=i).first(
    ) for i in users_spoken_to if i != current_name], key=lambda n: n.username)

    convo_vals = []
    for name in convo_keys:
        convo_vals.append([i for i in messages
                           if i.sender == name.username or i.receiver == name.username])

    convo_vals = [sorted(i, key=lambda n: n.id, reverse=True)
                  for i in convo_vals]
    user_list = [i for i in User.query.all() if i.username !=
                 current_user.username]

    return render_template('messages.html', user=current_user, convo_keys=convo_keys,
                           convo_vals=convo_vals,
                           user_list=user_list,
                           user_search=User.query.all(),
                           messages=messages)


@ app.route('/group-chat', methods=['GET', 'POST'])
@ login_required
def group_chat():
    messages = sorted(Chat.query.all(), key=lambda n: n.id, reverse=True)

    return render_template('groupchat.html', user=current_user,
                           user_search=User.query.all(),
                           messages=messages)


'''SOCKETIO EVENT HANDLERS'''


@ socketio.on('message')
@ login_required
def handle_message(message):
    print(f'Received message: {message}')
    if message != 'User connected!':
        if message != ' : ':
            new_message = Chat(sender=current_user.username,
                               text=message, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            send(message, broadcast=True)

        print(message)


users = {}


@ socketio.on('username', namespace='/private')
@ login_required
def receive_username(username):
    for user in User.query.all():
        users[user.username] = request.sid
    print(users)
    if username in users:
        users[username] = request.sid
        print('username added!')
    else:
        print('username not entered')


@ socketio.on('dm', namespace='/private')
@ login_required
def handle_dm(payload):
    print(payload)
    try:
        recipient_sess_id = users[payload['username'].lower()]
        message = payload['message']
        sender = current_user.username
        new_dm = Messages(
            sender=sender, receiver=payload['username'].lower(), text=payload['message'],
            user_id=current_user.id)
        db.session.add(new_dm)
        db.session.commit()
        emit('new_dm', message, room=recipient_sess_id)
        print('done emiting, no errors')
    except (KeyError, UnboundLocalError):
        pass


if __name__ == '__main__':
    socketio.run(app, host="localhost")
