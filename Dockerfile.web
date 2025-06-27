FROM python:3.12

WORKDIR /app/src

COPY requirements.txt requirements.txt


RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -U pip wheel && python -m pip install -r requirements.txt

COPY src /app/src
COPY /post-process/wait-for-it.sh /scripts/
