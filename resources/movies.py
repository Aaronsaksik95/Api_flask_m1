from flask import request, Response
from flask_restful import Resource
from classes.Movie import Movie
from mongoengine.errors import FieldDoesNotExist, \
    NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from .errors import SchemaValidationError, MovieAlreadyExistsError, \
    InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError


class MoviesController(Resource):
    def get(self):
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            movie = Movie(**body).save().to_json()
            return Response(movie, mimetype="application/json", status=201)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class MovieController(Resource):
    def get(self, id):
        movie = Movie.objects(id=id).to_json()
        return Response(movie, mimetype="application/json", status=200)

    def put(self, id):
        try:
            body = request.get_json()
            Movie.objects.get(id=id).update(**body)
            movie = self.get(id)
            return movie
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    def delete(self, id):
        try:
            Movie.objects.get(id=id).delete()
            return '', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError
