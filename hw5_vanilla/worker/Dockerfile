FROM python:3.6-alpine
RUN pip install redis
RUN pip install requests
COPY worker.py /
CMD ["python", "worker.py"]
