FROM python:3.12-alpine

LABEL authors="ruben"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
EXPOSE 8080
CMD ["uvicorn", "scr.main:app", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["uvicorn", "scr.main:app"]

