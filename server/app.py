#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize session['page_views'] to 0 if it doesn't exist
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views by 1 for each request
    session['page_views'] += 1

    # Check if page_views is greater than 3
    if session['page_views'] > 3:
        # Render JSON response with error message and status code 401
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    else:
        # Fetch article data from database
        article = Article.query.get(id)
        # Render JSON response with article data
        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content
        })

if __name__ == '__main__':
    app.run(port=5555)
