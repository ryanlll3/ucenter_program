FROM python:3.10
MAINTAINER RYANLLL3<ryanbetough@qq.com>
ENV PYTHONPATH "${PYTHONPATH}:/opt/ucenter_api"
ENV TIME_ZONE Asia/Shanghai

RUN mkdir -p /opt/ucenter_api/logs
COPY . /opt/ucenter_api/
WORKDIR /opt/ucenter_api
RUN chmod 777 -R * && \
    pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt && \
    ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone


ENTRYPOINT ["python", "./UCenter_API_Process.py"]