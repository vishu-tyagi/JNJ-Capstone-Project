ARG IMAGE
FROM ${IMAGE}

COPY . .

RUN pip install -e src/capstone

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]