uvicorn app.main:app --reload

docker build -t fastapi-ci-cd .

docker run -d -p 8000:8000 fastapi-ci-cd