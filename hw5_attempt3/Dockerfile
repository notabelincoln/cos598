FROM python:3.5-alpine
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
COPY templates/ /templates/
COPY static/ /static/
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
EXPOSE 5000
