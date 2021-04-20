FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

RUN pip install --target=/app requests
RUN pip install --target=/app -U pip setuptools pyminder
RUN pip install --target=/app ruamel.yaml

FROM gcr.io/distroless/python3-debian10:latest
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]