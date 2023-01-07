FROM python:3.11-slim

LABEL MAINTAINER="Xabier Iglesias <xabier.iglesias@coren.es>"

ENV GROUP_ID=1000 \
    USER_ID=1000

# Create app folder
RUN mkdir -p /server/app

# Copy app
ADD app/* /server/app/
ADD conf/* /server/conf/
COPY wsgi.py /server/wsgi.py
COPY requirements.txt /server/requirements.txt

WORKDIR /server/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --shell /bin/sh -u $USER_ID www --ingroup www

USER www

# Run the application
CMD ["gunicorn", "-w", "1", "--reload", "--bind", "0.0.0.0:5000", "wsgi"]