# The Garden Society API

Backend REST API for [The Garden Society](https://github.com/powellniki/gardenproject-client) which handles auth, posts, comments, discussion topics, gardener profiles, and image uploads.

## Tech Stack

- Django + Django REST Framework
- Token-based authentication (DRF authtoken)
- django-cors-headers
- SQLite
- Pillow (image uploads)

## Endpoints

| Endpoint | Description |
|---|---|
| `POST /register`, `POST /login` | Auth, returns a token |
| `/posts` | CRUD for discussion posts |
| `/topics` | Discussion topics |
| `/comments` | Comments on posts |
| `/images` | Photos attached to posts |
| `/profiles` | Gardener profiles |

## Getting Started

This is the backend half of a two-repo project. Pair it with the [client repo](https://github.com/powellniki/gardenproject-client).

1. Clone this repo
2. Install dependencies:
   ```
   pipenv install
   pipenv shell
   ```
3. Create a `.env` file in the project root:
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   DEVELOPMENT_MODE=True
   ```
4. Set up and seed the database:
   ```
   ./seed_database.sh
   ```
5. Run the server:
   ```
   python manage.py runserver
   ```
   The API will be live at `http://127.0.0.1:8000`.