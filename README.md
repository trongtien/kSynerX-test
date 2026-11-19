# KSynerx Test

## Work done and not done

### Done

- Api webhook input data
- Api import excel and export template excel data product

## Detail package using project

| Name                        | Note                                                         |
| --------------------------- | ------------------------------------------------------------ |
| FastAPI, uvicorn            | Framwork run API and run ASGI Server                         |
| pynatic-settings            | Support load setting enviroment file                         |
| sqlalchemy, psycopg2-binary | ORM and Driver connect and query database                    |
| pandas, openpyxl            | File processing and reading xslx, pandas format extract data |
| apscheduler                 | Run background app                                           |
| locust                      | Load test                                                    |

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

## Worflow and API prototype

- API webhook
  URL: api/webhook/products
  Method: POST
  Content-type: application/json

  Request body: array product change

  | Name | Type               | Note |
  | ---- | ------------------ | ---- |
  | sku  | string (requrired) |      |
  | name | string (requrired) |      |

  Response:

  | Name    | Type   | Note |
  | ------- | ------ | ---- |
  | status  | string |      |
  | total   | number |      |
  | created | number |      |
  | update  | number |      |

- API export teample xlsx product
  URL: api/excel/template-file-export
  Method: GET
  Content-type: application/octet-stream,
  Response: Streaming File
