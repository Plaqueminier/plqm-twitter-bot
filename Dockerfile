FROM python:3.10.4
WORKDIR /home/plqmnr/Documents/plqm-twitter-bot
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]