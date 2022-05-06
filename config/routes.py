from resources.movies import MoviesController, MovieController


def initialize_routes(api):
    api.add_resource(MoviesController, '/api/movies')
    api.add_resource(MovieController, '/api/movies/<string:id>')