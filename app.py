from flask import Flask, request, Response
from flask_restful import Api
from config.database import initialize_db
from routers.routes import initialize_routes
from models.errors import errors

app = Flask(__name__)
api = Api(app, errors=errors)

initialize_db(app)
initialize_routes(api)
