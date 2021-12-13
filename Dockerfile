FROM python:latest

WORKDIR /scraper

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /scraper/

CMD [ "python", "bb-scraper.py" ]
