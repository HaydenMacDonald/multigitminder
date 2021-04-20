FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

RUN pip install --target=/app --no-cache-dir requests
RUN pip install --target=/app --no-cache-dir -U pip setuptools pyminder
RUN pip install --target=/app --no-cache-dir ruamel.yaml

FROM gcr.io/distroless/python3-debian10@sha256:f6c3961ea6a177c21e31449e4833904e35434ba2038757771b0a2d3dc7958a31
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]