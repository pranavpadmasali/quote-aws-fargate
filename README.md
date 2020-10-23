REST backend for quote app.

# Steps to run locally
1. Clone the repository
2. Create a virtual environment with python 3.8. using command 
```bash
python3 -m venv venv
```
3. Source virtual environment by
```
source venv/bin/activate
```
4. Add the environment variables
```bash
export MONGO_DB_PASSWORD=YOUR_DB_PASSWORD
export MONGO_DB_USERNAME=YOUR_USERNAME
```
5. Run the flask app with development server.
```bash
python app.py
```
To run flask with production server use gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```
6. To build the docker image locally run 
```bash
docker build  --build-arg  mongo_username=YOUR_USERNAME --build-arg mongo_password=YOUR_DB_PASSWORD -t quotes-app .
```
7. To run the docker image locally run 
```bash
docker run -d -p 9988:5000 quotes-app 
```

# Testing
The backend is deployed on aws fargate and aws gateway is currently used to terminate https and proxy the request to fargate task.

## Get All quotes
```bash
curl --location --request GET 'https://2zbus46lel.execute-api.ap-south-1.amazonaws.com/v1/quote'
```
## Get rated quotes
```bash
curl --location --request GET 'https://2zbus46lel.execute-api.ap-south-1.amazonaws.com/v1/getRatedQuote'
```

## Update quote with rating
```bash
curl --location --request PUT 'https://2zbus46lel.execute-api.ap-south-1.amazonaws.com/v1/quote/5aa45f317832df00040ac9c0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "rating":4
}'
```

## Get related quote similarity 
```bash
curl --location --request POST 'https://2zbus46lel.execute-api.ap-south-1.amazonaws.com/v1/getRelatedQuote' \
--header 'Content-Type: application/json' \
--data-raw '{"quote":"automating your work is creativity"}'
```

## Add new quote
```bash
curl --location --request POST 'https://2zbus46lel.execute-api.ap-south-1.amazonaws.com/v1/quote' \
--header 'Content-Type: application/json' \
--data-raw '{
    "quotes":"here and there",
    "author":"George O",
    "rating":4
}'
```
