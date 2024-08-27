FROM python:3.10

WORKDIR /app

# For pg_isready command
RUN apt-get update && apt-get install -y postgresql-client

COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pip install pipenv && pipenv install --system --deploy

# Install doit
RUN pip install doit

# Copy only the necessary application files
COPY ./vocabulary_builder /app/vocabulary_builder
COPY ./docker/entrypoint.sh /app/entrypoint.sh
COPY ./tiny_db_input.json /app/tiny_db_input.json
COPY .env /app/.env
COPY dodo.py /app/dodo.py
COPY locales /app/locales
COPY babel.cfg /app/babel.cfg

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "vocabulary_builder.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
