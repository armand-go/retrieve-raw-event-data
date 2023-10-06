FROM python:3.11
WORKDIR /home/app

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install python dependencies in venv
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

# Install application into container
COPY . /home/app
