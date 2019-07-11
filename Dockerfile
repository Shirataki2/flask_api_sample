FROM python:3.7

ARG project_dir=/src/

ADD src/requirements.txt $project_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt
