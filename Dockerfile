FROM python:3.13-slim
LABEL org.opencontainers.image.source="https://github.com/mroshdy91/SupplierAtlas-Demo"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 SUPPLIER_ATLAS_DB=/app/data/catalog.sqlite
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --no-deps . && useradd --uid 10001 --create-home atlas
COPY --chown=atlas:atlas data/catalog.sqlite ./data/catalog.sqlite
USER atlas
EXPOSE 8080
CMD ["supplier-atlas", "--transport", "http", "--host", "0.0.0.0"]
