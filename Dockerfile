FROM python:3.5.2
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /code
ADD . /code
ENV FLASK_DEBUG=1
ENV FLASK_APP=app.py
CMD flask run --host=0.0.0.0