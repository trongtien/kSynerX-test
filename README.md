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
| pynatic-settings            | Support load setting enviroment file                         |
| sqlalchemy, psycopg2-binary | ORM and Driver connect and query database                    |
| pandas, openpyxl            | File processing and reading xslx, pandas format extract data |
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

## Work done and not done

### Done

- Api webhook input data
- Api import excel and export template excel data product

## Database Schema

- Table Products

| Name           | Type                                 | Note                        |
| -------------- | ------------------------------------ | --------------------------- |
| sku            | VARCHAR(100)                         | Primary                     |
| parner_sku     | VARCHAR(100)                         |                             |
| product_name   | VARCHAR(255)                         | NOT NUll                    |
| product_name   | VARCHAR(255)                         | NOT NUll                    |
| asset_type     | VARCHAR(30)                          |                             |
| color          | VARCHAR(100)                         |                             |
| color          | VARCHAR(100)                         |                             |
| description    | TEXT                                 |                             |
| has_serial     | BOOLEAN                              |                             |
| has_expiration | BOOLEAN                              |                             |
| is_active      | boolean                              | NOT NUll, default True      |
| units          | JSONB                                | NOT NUll, default []        |
| categories     | JSONB                                | NOT NUll, default []        |
| last_source    | enum ('POLLING', 'WEBHOOK', 'EXCEL') | NOT NULL                    |
| created_at     | TIMESTAMP(64)                        | NOT NUll, default timestamp |
| updated_at     | TIMESTAMP(64)                        | NOT NUll, default timestamp |

- Table Product audit log

| Name        | Type                                  | Note                        |
| ----------- | ------------------------------------- | --------------------------- |
| id          | BIGINT                                | Primary                     |
| sku         | VARCHAR(100)                          | NOT NUll                    |
| change_type | enum('CREATED', 'UPDATED', 'SKIPPED') | NOT NUll                    |
| details     | JSONB                                 |                             |
| created_at  | TIMESTAMP                             | NOT NUll, default timestamp |

- Table Ingestion log

| Name          | Type                 | Note                        |
| ------------- | -------------------- | --------------------------- |
| id            | BIGINT               | Primary                     |
| source_type   | VARCHAR(50)          | NOT NUll                    |
| status        | enum(WEBHOOK, EXCEL) | NOT NUll                    |
| total_records | INTEGER              | NOT NULL, default 0         |
| created_count | INTEGER              | NOT NULL, default 0         |
| skipped_count | INTEGER              | NOT NULL, default 0         |
| created_at    | TIMESTAMP            | NOT NUll, default timestamp |
