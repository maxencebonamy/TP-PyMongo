# Movie Database API

This project is a FastAPI application that interacts with MongoDB and Neo4j to provide APIs for movie and people data. It includes features to query common movies, people who rated specific movies, and details about people ratings.

## Features
- List all movies
`GET /movies`
- List a specific movie - the name of the movie or the name of the actor are given in parameter 
`GET /movies?title_filter=Titanic`
`GET /movies?actor_filter=DiCaprio`
- Update information about a specific movie - the name of the movie is given in parameter
`PATCH /movies/Titanic`
- Return the number of movies common between mongoDB database & neo4j database 
`GET /movies/common`
- List users who rated a movie - the name of the movie is given in parameter 
`GET /movies/people_who_rated?title=Titanic`
- Return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter 
`GET /movies/rating?person_name=Leonardo`
---

## Requirements
### Prerequisites
- Python 3.8 or higher
- MongoDB instance with a `movies` collection
- Neo4j instance with `Person`, `Movie`, and `REVIEWED` relationships
- Installed **pip** for Python package management

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maxencebonamy/pymongo.git
   cd pymongo
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables by creating a `.env` file in the project root following .env.example structure.

---

## Running the Application

1. Start MongoDB and Neo4j servers if they are not already running.

2. Run the FastAPI application:
   ```bash
   fastapi run src/main.py
   ```

3. Access the API documentation at:
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Troubleshooting

- **MongoDB Connection Issues**: Ensure the `MONGODB_URL` is correct and the MongoDB server is running.
- **Neo4j Connection Issues**: Verify `NEO4J_URL`, username, and password in the `.env` file.
- **Dependency Issues**: Run `pip install -r requirements.txt` to ensure all dependencies are installed.
