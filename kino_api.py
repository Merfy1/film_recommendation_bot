import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("KINOPOISK_API_KEY")

class KinoAPI:
    def __init__(self):
        self.base_url = 'https://api.kinopoisk.dev/v1.3/movie'
        self.headers = {
            'X-API-KEY': API_TOKEN,
            'Content-Type': 'application/json'
        }

    def get_movies_by_genre(self, genre_name):
        params = {
            'genres.name': genre_name,
            'limit': 10
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'docs' in data:
                movies = data['docs']
                if not movies:
                    return "Фильмы не найдены по выбранному жанру."
                random_movie = random.choice(movies)
                return self.format_movie_info(random_movie)
            else:
                return "Фильмы не найдены по выбранному жанру."
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return "Не удалось получить фильмы по жанру, попробуйте снова позже."

    def get_movie_by_name(self, movie_name):
        movie_name = movie_name.strip().title()
        params = {
            'name': movie_name,
            'limit': 1
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            movies = data.get('docs', [])
            if not movies:
                return "Фильм с таким названием не найден."
            return self.format_movie_info(movies[0])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return "Не удалось найти фильм, попробуйте снова позже."

    def get_movie_by_year(self, year):
        params = {
            'year': year,
            'limit': 10
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'docs' in data:
                movies = data['docs']
                if not movies:
                    return f"Фильмы за {year} год не найдены."
                random_movie = random.choice(movies)
                return self.format_movie_info(random_movie)
            else:
                return f"Фильмы за {year} год не найдены."
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return "Не удалось найти фильмы за указанный год, попробуйте снова позже."

    def get_movie_by_person(self, person_name):
        params = {
            'persons.name': person_name.strip().title(),
            'limit': 10
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'docs' in data:
                movies = data['docs']
                if not movies:
                    return f"Фильмы с участием или под руководством {person_name} не найдены."
                random_movie = random.choice(movies)
                return self.format_movie_info(random_movie)
            else:
                return f"Фильмы с участием или под руководством {person_name} не найдены."
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return "Не удалось найти фильмы по человеку, попробуйте снова позже."

    def get_random_movie(self):
        max_retries = 100
        for _ in range(max_retries):
            random_id = random.randint(300, 999999)
            print(f"Пробуем найти фильм с ID: {random_id}")
            try:
                response = requests.get(f"{self.base_url}/{random_id}", headers=self.headers)
                response.raise_for_status()
                data = response.json()

                if data and data.get('name'):
                    return self.format_movie_info(data)
            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    continue
                else:
                    print(f"Ошибка при запросе к API: {e}")
                    return "Не удалось найти фильм, попробуйте снова позже."
        return "Не удалось найти случайный фильм после нескольких попыток. Попробуйте снова позже."

    def format_movie_info(self, movie):
        name = movie.get('name', 'Без названия')
        year = movie.get('year', 'Неизвестно')
        description = movie.get('description', 'Нет описания')
        poster_url = movie.get('poster', {}).get('url', None)
        genres = ", ".join(genre.get('name', '') for genre in movie.get('genres', []))

        movie_details = f"Название: {name}\nГод: {year}\nЖанры: {genres if genres else 'Нет данных'}\nОписание: {description if description else 'Нет описания'}"
        if poster_url:
            movie_details += f"\nПостер: {poster_url}"
        return movie_details

