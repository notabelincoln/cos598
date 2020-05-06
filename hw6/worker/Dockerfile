FROM python:3.6-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
ENV FLASK_APP worker.py
ENV FLASK_RUN HOST 0.0.0.0
RUN pip install redis
RUN pip install requests
RUN pip install flask
COPY worker.py /
COPY . .
CMD ["flask", "run"]
EXPOSE 80
