FROM python:3.10-slim
WORKDIR /weather_api
COPY requirements.txt /weather_api
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8989
CMD ["gunicorn", "-b", "0.0.0.0:8989", "application:application"]


