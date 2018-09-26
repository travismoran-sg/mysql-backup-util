# mysql backup image
FROM alpine:3.7
MAINTAINER Travis Moran

# install the necessary client
RUN apk add --update mysql-client bash python3 samba-client \
    python py-setuptools py3-dateutil py3-magic python3 \
    wget tar bash supervisor && \
    rm -rf /var/cache/apk/*


RUN cd /tmp && \
	wget 'https://downloads.sourceforge.net/project/s3tools/s3cmd/2.0.2/s3cmd-2.0.2.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fs3tools%2Ffiles%2Fs3cmd%2F2.0.2%2Fs3cmd-2.0.2.tar.gz%2Fdownload&ts=1537919988' -O 's3cmd-2.0.2.tar.gz' && \
	tar xfvz s3cmd-2.0.2.tar.gz && cd s3cmd-2.0.2 && \
	python setup.py install

ENV NAME DB_HOST
ENV NAME DB_USER
ENV NAME DB_PASSWORD
ENV NAME DB_NAME
ENV NAME BACKUP_PATH

# install the entrypoint
COPY supervisord.conf /etc/supervisord.conf
COPY s3cfg /root/.s3cfg
COPY entrypoint.py /usr/local/bin/entrypoint.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# start
CMD ["/usr/bin/supervisord", "-n"]
