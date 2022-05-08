import requests
from tests.test_base import TestBase


class TestMovie(TestBase):

    def test_create_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        response = requests.post('http://127.0.0.1:5000/api/movies', json=data)
        movie_create = response.json()

        self.assertEqual("Harry Potter", movie_create["name"])
        self.assertEqual(201, response.status_code)

    def test_get_movies(self):
        response = requests.get('http://127.0.0.1:5000/api/movies')
        movies = response.json()

        self.assertGreater(len(movies), 0)
        self.assertEqual(200, response.status_code)

    def test_get_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        response_create = requests.post(
            'http://127.0.0.1:5000/api/movies', json=data)
        movie_id = response_create.json()['_id']['$oid']
        response_get = requests.get(
            f'http://127.0.0.1:5000/api/movies/{movie_id}')
        movie_get = response_get.json()

        self.assertEqual("Harry Potter", movie_get[0]["name"])
        self.assertEqual(200, response_get.status_code)

    def test_update_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"]
        }
        data_update = {
            "name": "Star Wars",
            "casts": ["Hayden Christensen", "Ewan McGregor"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        response_create = requests.post(
            'http://127.0.0.1:5000/api/movies', json=data)
        movie_id = response_create.json()['_id']['$oid']
        response_update = requests.put(
            f'http://127.0.0.1:5000/api/movies/{movie_id}', json=data_update)
        movie_update = response_update.json()

        self.assertEqual("Star Wars", movie_update[0]["name"])
        self.assertEqual(["Hayden Christensen", "Ewan McGregor"],
                         movie_update[0]["casts"])
        self.assertEqual(200, response_update.status_code)

    def test_delete_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        response_create = requests.post(
            'http://127.0.0.1:5000/api/movies', json=data)
        movie_id = response_create.json()['_id']['$oid']
        response_delete = requests.delete(
            f'http://127.0.0.1:5000/api/movies/{movie_id}')

        self.assertEqual(200, response_delete.status_code)



class TestMovieError(TestBase):

    def test_create_field_does_not_exist_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"],
            "FieldNotExist": "TestException"
        }
        response = requests.post('http://127.0.0.1:5000/api/movies', json=data)
        error = response.json()
        self.assertEqual("Request is missing required fields",
                         error["message"])
        self.assertEqual(400, response.status_code)

    def test_create_existing_movie(self):
        self.drop_db()
        data = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"],
        }
        data_same = {
            "name": "Harry Potter",
            "casts": ["daniel radcliffe", "Emma Watson"],
            "genres": ["Fantasy", "Sci-fi"],
        }
        requests.post('http://127.0.0.1:5000/api/movies', json=data)
        response = requests.post(
            'http://127.0.0.1:5000/api/movies', json=data_same)
        error = response.json()
        self.assertEqual(
            "Movie with given name already exists", error["message"])
        self.assertEqual(400, response.status_code)
