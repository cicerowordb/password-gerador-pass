FROM     python:3.7.14-alpine3.16
LABEL    owner cicerow
LABEL    base_image python_3.7.14_alpine3.16
LABEL    app password-gen
WORKDIR  /opt/app/
RUN      adduser --home /opt/app --disabled-password user
COPY     main.py /opt/app/
COPY     requirements.txt /opt/app
RUN      pip3 install -r requirements.txt --no-warn-script-location
CMD      ["/usr/local/bin/python","/opt/app/main.py"]
