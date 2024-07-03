FROM python:3.11.9-slim-bookworm

ARG BUILD_ENVIRONMENT=dev
# ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv==2023.9.8
ENV PIPENV_VENV_IN_PROJECT=1
COPY Pipfile Pipfile.lock ./
# for dev
RUN pipenv sync --dev
# for prod
# RUN pipenv sync
ENV PATH=${APP_HOME}/.venv/bin:${PATH}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY . ${APP_HOME}

ENV DJANGO_READ_DOT_ENV_FILE=true

RUN DATABASE_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  python manage.py compilemessages

ENTRYPOINT ["/entrypoint.sh"]
