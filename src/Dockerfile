FROM python:3.6.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /tvshows-bot
WORKDIR /tvshows-bot

# Copy all sources
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9706
