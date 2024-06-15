FROM ubuntu:20.04

WORKDIR /main
COPY . ./

RUN apt update && apt install -y python3
RUN chmod +x find_mtu.py

CMD [ "./find_mtu.py", "--host=google.com" ]
