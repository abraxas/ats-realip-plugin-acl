FROM ats-10.2.0-lab:local

ARG RECORDS_FILE=records-plugin.yaml

USER root
COPY conf/remap.config /opt/ats/etc/trafficserver/remap.config
COPY conf/ip_allow.yaml /opt/ats/etc/trafficserver/ip_allow.yaml
COPY conf/plugin.config /opt/ats/etc/trafficserver/plugin.config
COPY conf/realip.yaml /opt/ats/etc/trafficserver/realip.yaml
COPY conf/storage.config /opt/ats/etc/trafficserver/storage.config
COPY conf/${RECORDS_FILE} /opt/ats/etc/trafficserver/records.yaml
RUN mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver \
 && chown -R nobody:nogroup /opt/ats/var \
 && test -f /opt/ats/libexec/trafficserver/realip.so \
 && /opt/ats/bin/traffic_server --version

EXPOSE 8080
CMD ["traffic_server"]
