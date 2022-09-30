import flask
from data import db_session
from data.news import News
from flask import jsonify
from flask import request


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name')) for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()

    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'news': news.to_dict(only=('title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    content = request.json

    if not content:
        return jsonify({'error': 'Empty request'})
    elif not all(key in content for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    news = News(
        title=content['title'],
        content=content['content'],
        user_id=content['user_id'],
        is_private=content['is_private']
    )
    db_sess.add(news)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


