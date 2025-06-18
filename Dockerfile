#env version from where we start
FROM python:3.11-slim

# this is environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1



#specifing working directory you can come up with any name
WORKDIR /app 


# coping requirements.txt file for our working directory
COPY requirements.txt .


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# after all we copy 
COPY . .

EXPOSE 8000


CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"


