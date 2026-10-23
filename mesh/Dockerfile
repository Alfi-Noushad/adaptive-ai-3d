FROM python:3.11-slim

WORKDIR /app

COPY mesh/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY mesh ./mesh

ENV MESH_STORAGE_ROOT=/shared
EXPOSE 8002

CMD ["uvicorn", "mesh.api.main:app", "--host", "0.0.0.0", "--port", "8002"]
