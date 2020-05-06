FROM python:3.5-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
COPY coworker.py /
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "coworker.py"]
EXPOSE 80
