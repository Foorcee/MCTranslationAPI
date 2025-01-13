FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('Foorcee/t5-minecraft-de-en-base', cache_dir='/code/model')"
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('Foorcee/t5-minecraft-de-en-base', cache_dir='/code/model')"


COPY ./app /code/app

EXPOSE 80
CMD ["fastapi", "run", "app/main.py", "--port", "80"]