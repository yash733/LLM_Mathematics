FROM python:3.9
WORKDIR /Maths_problem
COPY . /Maths_problem
EXPOSE 8501
RUN pip install -r requirement.txt
CMD []