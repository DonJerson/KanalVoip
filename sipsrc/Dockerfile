FROM debian:stable-slim

RUN apt-get update && apt-get install -y kamailio kamailio-mysql-modules kamailio-extra-modules kamailio-outbound-modules
COPY kamailio.cfg /etc/kamailio/kamailio.cfg

ENTRYPOINT ["kamailio", "-DD", "-E", "-f", "/etc/kamailio/kamailio.cfg"]