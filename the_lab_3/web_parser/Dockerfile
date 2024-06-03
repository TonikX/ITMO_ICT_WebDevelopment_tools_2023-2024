# 
FROM python:3.10.5

# 
WORKDIR /web_parser

# 
COPY ./requirements.txt /site/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /site/requirements.txt

# 
COPY . .
