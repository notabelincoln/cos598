FROM alpine:latest
RUN apk add --update sqlite
RUN mkdir ./db
WORKDIR ./db

ENTRYPOINT ["sqlite3"]
CMD ["jordan_container.db"]
