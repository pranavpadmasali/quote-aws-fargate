FROM python:3.8 
RUN mkdir /app
COPY . /app
WORKDIR /app
ARG mongo_username
ARG mongo_password
ENV MONGO_DB_USERNAME=$mongo_username
ENV MONGO_DB_PASSWORD=$mongo_password
RUN pip install -r requirements.txt 
RUN python -m spacy download en_core_web_lg 
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 --chdir /app app:app