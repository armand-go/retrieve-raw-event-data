# TECHNICAL TEST: Retrieve raw events data

The aim of this README is to explain the choices made during API development as part of the technical test.

### Technologies used

This API is developed in **Python** using the **FastAPI** framework, both because it's the language Billy uses on the backend, and because it's the technology I work with every day. The database used is **PostgreSQL** for the same reasons.

Data models are managed with **SQLAlchemy**, while the various data migrations are handled with **yoyo-migrations**.

### Distribution

3 docker containers were used for this test: the first for the Python development environment, a second for the PostgreSQL database, the third launching the API. Once launched, the API can be accessed at http://localhost:8000

#### VSCode dev container

If you use VSCode, it is best to run the project in container using the DevContainer feature. It will use a standardized environements and configuration ensuring linters are active.

To run inside the container:

- Maj+Ctrl+P
- Reopen in container

Git is directly usable from container instance. Feel free to change and configure your local instance at your convenience.

While running inside the container, API logs can be accessed through a terminal outside the container using `docker logs -f technical_test_api`.

#### Docker compose

Run `docker-compose up` from root directory. Then you can access logs using `docker logs -f technical_test_api`

### Project Organization

All the features are developped inside the app folder. The `app.py` serve as a hook for the API to be ran.

The project is organized along the hexagonal lines. The "User-Side" part is in the [swagger generated automatically by FastAPI](http://localhost:8000/docs). (Accessible when the API is launched).
The "Business Logic" is found in the various Usecases, while the "Server Side" is found in the adapters.
The various bricks are completed in the [dependencies.py](app/dependencies.py) file while the routes are added in this [**init**](app/__init__.py) file.

### Import the data

In order to import data, once the container is up and running, it is first necessary to perform the migration with yoyo. To do this, simply enter the `yoyo apply` command in the container console and wait for the migrations to complete.
You can then import the data by executing `python import_data.py` in your container's console. The data will then be imported.

### Trigger the API's endpoints

Go to [Swagger](http://localhost:8000/docs) and play with the differents endpoints available.

- _We want to be able to see a complete list of our events._: Use the endpoint `GET /events/list` without any parameter.
- _We want to filter this list using the event sale start time._ Use the endpoint `GET /events/list` and filter by the parameter you want. You can also define the operator (by default, it's ">=").
- _We want to be able to request a particular event using its id._ Use the endpoint `GET /events/withTicketCollection/{id}`. It will return the event with the same format specified in the [Usecase](README_OLD.md#use-case). If you only want the Event without the associated ticket collections, use the endpoint `GET /events/{id}`
- _We want to be able to update an event data (the event title, the line up, the image or video url and collection name)_ Two possibilities here: modify the data in the `.csv` or the `.json` file and then, re-run the `python import_data.py` command. Or else, you can call the endpoint `PUT /event/{id}` and `PUT /smartContracts/{id}` and add to the body the value you want to modify. The values are all optional.
