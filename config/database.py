from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb+srv://aaronsaksik:azertyuiop@cluster0.4jhow.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    }

    db.init_app(app)
