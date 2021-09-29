FROM python:3.8

COPY main.py .

# RUN pip install os_sys

CMD ["python", "./main.py"]