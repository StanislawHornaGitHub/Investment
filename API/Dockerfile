FROM ubuntu:latest
RUN apt update
RUN apt install -y python3-dev 
RUN apt install -y pip
RUN pip install --upgrade pip
WORKDIR /App
COPY . /App
RUN pip install requests
RUN pip install flask
RUN pip install psycopg2-binary
RUN pip install SQLAlchemy
CMD ["python3", "./App/Investment_API.py"]