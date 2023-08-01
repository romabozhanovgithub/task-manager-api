FROM python:3.10.9 as base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT
RUN env

FROM base as base-dev
RUN pip install --no-cache pipenv
COPY Pipfile* .
RUN PIP_USER=1 pipenv install --system --deploy --dev

FROM base-dev as dev

COPY --from=base-dev $PYROOT/lib $PYROOT/lib

WORKDIR /app

COPY . .

RUN chmod +x ./scripts/wait_for_postgres.py
RUN chmod +x ./scripts/entrypoint.sh

ENTRYPOINT [ "sh", "./scripts/entrypoint.sh" ]
