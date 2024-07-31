FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Print directory contents for debugging purposes
RUN ls -la /app/templates
RUN ls -la /app/static
RUN ls -la /app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
