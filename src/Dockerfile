FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /usr/sbin/nologin appuser && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip openssh-server sudo && \
    useradd -m -s /bin/bash pedro && \
    useradd -m -s /bin/bash adrian && \
    chmod 700 /home/adrian && chmod 700 /home/pedro && \
    echo 'MyFlag{bR6flq_2x}' > '/home/adrian/flag.txt' && \
    echo 'MyFlag{84z5k6_tt}' > '/home/pedro/flag.txt' && \
    echo 'MyFlag{53ozzv_g1}' > '/root/flag.txt' && \
    echo 'pedro:jamonconmelon' | chpasswd && \
    echo 'adrian:GHufgiu9_sdsd9' | chpasswd && \
    echo 'pedro ALL=(ALL) /bin/find' >> /etc/sudoers && \
    sed -i "s/pedro:x/pedro:$(printf '%s\n' "$(grep "^pedro:" /etc/shadow | cut -d: -f2)" | sed -e 's/[\/&]/\\&/g')/" /etc/passwd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#ChallengeResponseAuthentication yes/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication no/' /etc/ssh/sshd_config

COPY ./server /home/adrian/app
WORKDIR /home/adrian/app
RUN chown -R root:root /home/adrian/app && chmod +x /home/adrian/app/check_command.sh

RUN pip install -r requirements.txt

EXPOSE 42424
EXPOSE 4242
EXPOSE 22

RUN mkdir /var/run/sshd
CMD ["/bin/bash", "-c", "/usr/sbin/sshd && sudo -u adrian python3 server.py"]
