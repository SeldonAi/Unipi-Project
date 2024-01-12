FROM python:3.9.18-slim 
WORKDIR /math_py
ADD . .
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
