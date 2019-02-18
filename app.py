from flask import Flask,jsonify, request
from flask.json import JSONEncoder

"""
기본 json encoder 는 set 을 json 으로 변환 할 수 없다.
custom encoder 를 작성하여 set 을 list 로 변환하여 json 으로 변환 가능 하게 해주어야 한다. 
"""
class CustomJSONENcoder(JSONEncoder):
    def default(self, o):
        if isinstance(o,set):
            return list()
        return JSONEncoder.default(self,o)


app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []
app.json_encoder = CustomJSONENcoder


@app.route('/ping')
def health():
    return 'pong'


@app.route('/sign-up',methods=['POST'])
def sign_up():
    new_user = request.json
    new_user['id'] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)


@app.route('/tweet',methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return 'user not found', 400

    if len(tweet) > 300:
        return 'Over 300 character', 400

    user_id = int(payload['id'])
    app.tweets.append({
        'user_id': user_id,'tweet': tweet
    })
    return '', 200


@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return 'user not found', 400
    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)
    return jsonify(user)


@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return 'user not found', 400
    user = app.users[user_id]
    user.setdefault('unfollow', set()).discard(user_id_to_follow)
    return jsonify(user)


@app.route('/timeline/<int:user_id>',methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'user not found'

    follow_list = app.users[user_id].get('follow',set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]
    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })


if __name__ == '__main__':
    app.run()
