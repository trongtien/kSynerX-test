# KSynerx Test

## Overide

- Service cdms: api run port 3000
- Service loadtest : api run port 4000

## Run service

- docker compose up --build -d
- Swgger:
  - cdms: http://localhost:3000/docs
  - loadtes: http://localhost:4000/docs
- Run local not docker: python cdms/main.py, python loadtest/main.py
  - cdms: python cdms/main.py
  - loadtes: loadtest/main.py

## Detail package using project

| Name                        | Note                                                         |
| --------------------------- | ------------------------------------------------------------ |
| FastAPI, uvicorn            | Framwork run API and run ASGI Server                         |
| pydantic                    | Validate request body and define data schema                 |
| pydantic-settings           | Support load setting enviroment file                         |
| python-dotenv               | Read file .env (used by pydantic-settings env_file)          |
| python-multipart            | Parse multipart/form-data upload file excel (UploadFile)     |
| sqlalchemy, psycopg2-binary | ORM and Driver connect and query database                    |
| pandas, openpyxl            | File processing and reading xslx, pandas format extract data |
| httpx                       | HTTP client cdms call service loadtest pull data product     |
| faker                       | Generator data testing                                       |

## Configuaration

| Name                          | Value              | Note                       |
| ----------------------------- | ------------------ | -------------------------- |
| SERVICE_HOST                  | locahost (default) | Item3.1                    |
| SERVICE_PORT                  | 3000 (default)     | Item3.1                    |
| SERVICE_TEST_HOST             | locahost (default) | Item3.1                    |
| SERVICE_TEST_PORT             | 40000 (default)    | Item3.1                    |
| DATABASE_HOST                 | required           | Host database postgres     |
| DATABASE_PORT                 | required           | Port database postgres     |
| DATABASE_DB_NAMME             | required           | Db name database postgres  |
| DATABASE_DB_USERNAME          | required           | Usernane database postgres |
| PULL_PRODUCT_INTERVAL_SECONDS | 300                | Time fetch data product    |
| PULL_PRODUCT_PAGE_SIZE        | 100                | Size page fetch Product    |
| PULL_PRODUCT_MAX_PAGE         | 1000               | Page max fetch product     |

## Worflow and API prototype

- API Headlh check
  URL: /
  Method: GET
  Content-type: application/json

- API webhook insert data product
  URL: api/webhook/products
  Method: POST
  Content-type: application/json

  Request body: array product change

  | Name     | Type            | Note |
  | -------- | --------------- | ---- |
  | products | ProductReqeuest |      |
  - sku, product_name: reqired not empty

- API export teample xlsx product
  URL: api/excel/template-file-export
  Method: GET
  Content-type: application/octet-stream,
  Response: Streaming File

- API product import
  URL: api/excel/product-import
  Method: POST
  Content-type: application/octet-stream, miltipart

## Database Schema

File script: `scripts/schema.sql`

- Enum

| Name                       | Value                         |
| -------------------------- | ----------------------------- |
| product_last_source_enum   | 'POLLING', 'WEBHOOK', 'EXCEL' |
| source_type_enum           | 'WEBHOOK', 'EXCEL', 'POLLING' |
| audit_log_change_type_enum | 'CREATED', 'UPDATED'          |

- Table products

| Name              | Type                     | Note                                                   |
| ----------------- | ------------------------ | ------------------------------------------------------ |
| sku               | VARCHAR(100)             | Primary                                                |
| product_id        | INTEGER                  |                                                        |
| partner_sku       | VARCHAR(100)             | Index idx_products_partner_sku                         |
| product_name      | VARCHAR(255)             | NOT NULL                                               |
| asset_type        | VARCHAR(30)              |                                                        |
| color             | VARCHAR(100)             |                                                        |
| size              | VARCHAR(100)             |                                                        |
| description       | TEXT                     |                                                        |
| has_serial        | BOOLEAN                  | NOT NULL, default FALSE                                |
| has_expiration    | BOOLEAN                  | NOT NULL, default FALSE                                |
| is_active         | BOOLEAN                  | NOT NULL, default TRUE                                 |
| units             | JSONB                    | NOT NULL, default []                                   |
| categories        | JSONB                    | NOT NULL, default []                                   |
| checksum_hash     | CHAR(64)                 | NOT NULL, hash data product detect change              |
| source_updated_at | TIMESTAMPTZ              | NOT NULL, time updated from source                     |
| last_source       | product_last_source_enum | NOT NULL                                               |
| created_at        | TIMESTAMPTZ              | NOT NULL, default now()                                |
| updated_at        | TIMESTAMPTZ              | NOT NULL, default now(), Index idx_products_updated_at |

- Table product_audit_log

| Name              | Type                       | Note                                                |
| ----------------- | -------------------------- | --------------------------------------------------- |
| id                | BIGINT                     | Primary, identity                                   |
| sku               | VARCHAR(100)               | NOT NULL, FK products(sku) ON DELETE RESTRICT       |
| change_type       | audit_log_change_type_enum | NOT NULL                                            |
| source_type       | source_type_enum           | NOT NULL                                            |
| ingestion_id      | BIGINT                     | FK ingestion_logs(id), Index idx_audit_ingestion_id |
| event_key         | VARCHAR(255)               |                                                     |
| checksum_hash     | CHAR(64)                   | NOT NULL                                            |
| details           | JSONB                      |                                                     |
| source_updated_at | TIMESTAMPTZ                | NOT NULL                                            |
| created_at        | TIMESTAMPTZ                | NOT NULL, default now()                             |

- Index idx_audit_sku_created_at: (sku, created_at)
- Unique index uq_audit_one_created_per_sku: (sku) WHERE change_type = 'CREATED' -> each sku only one log CREATED

- Table ingestion_logs

| Name          | Type             | Note                                                         |
| ------------- | ---------------- | ------------------------------------------------------------ |
| id            | BIGINT           | Primary, identity                                            |
| source_type   | source_type_enum | NOT NULL                                                     |
| status        | VARCHAR(30)      | NOT NULL                                                     |
| total_records | INTEGER          | NOT NULL, default 0                                          |
| created_count | INTEGER          | NOT NULL, default 0                                          |
| updated_count | INTEGER          | NOT NULL, default 0                                          |
| skipped_count | INTEGER          | NOT NULL, default 0                                          |
| created_at    | TIMESTAMPTZ      | NOT NULL, default now(), Index idx_ingestion_logs_created_at |

## Implemented / Not implemented

- Implemented
  - api data input
  - Change detection via hashing
  - Audit log
  - Ingestion log
  - Excel template
  - Emulator supports GET requests only
  - Run via Docker

- Not Implemented
  - Retry and backoff mechanisms for polling
  - 'FAILED' status in ingestion_logs
  - Retry connect database failed
  - Spike testing and concurrency testing
  - Detection of deleted products
