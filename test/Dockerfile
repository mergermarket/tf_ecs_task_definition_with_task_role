FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.11.2
ENV TERRAFORM_ZIP=terraform_${TERRAFORM_VERSION}_linux_amd64.zip
ENV TERRAFORM_SUM=f728fa73ff2a4c4235a28de4019802531758c7c090b6ca4c024d48063ab8537b

ENV PYTHONDONTWRITEBYTECODE donot

RUN apk add -U ca-certificates curl git && \
    cd /tmp && \
    curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${TERRAFORM_ZIP} && \
    echo "${TERRAFORM_SUM}  /tmp/${TERRAFORM_ZIP}" | sha256sum -c - && \
    unzip /tmp/${TERRAFORM_ZIP} -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
