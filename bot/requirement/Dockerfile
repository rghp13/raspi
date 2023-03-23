FROM ubuntu:20.04
RUN apt-get update && apt-get install -y tzdata
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris
RUN apt-get -y update
RUN apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev python3.9-full python3-pip
RUN python3 -m pip install -U discord.py requests wikipedia openai python-dotenv
EXPOSE 8082:80
EXPOSE 4432:443
COPY ./tool/discbot.py ./
COPY ./.env ./
COPY ./tool/haddock.txt ./
#COPY entry.sh ./
ENTRYPOINT ["python3", "./discbot.py"]