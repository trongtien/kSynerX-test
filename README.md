- KSynerx Test

- Database Schema

** Table Products

| Name          | Type          | Note                        |
| ------------- | ------------- | --------------------------- |
| sku           | VARCHAR(100)  | Primary                     |
| parner_sku    | VARCHAR(100)  |                             |
| name          | VARCHAR(255)  | NOT NUll                    |
| price         | NUMERIC(10,2) | NOT NUll (price >= 0)       |
| checksum_hash | VARCHAR(64)   | NOT NUll                    |
| is_active     | boolean       | NOT NUll                    |
| updated_at    | TIMESTAMP(64) | NOT NUll, default timestamp |

** Table Product audit log

| Name        | Type         | Note                                       |
| ----------- | ------------ | ------------------------------------------ |
| id          | BIGINT       | Primary                                    |
| sku         | VARCHAR(100) | NOT NUll                                   |
| change_type | VARCHAR(20)  | NOT NUll ('CREATED', 'UPDATED', 'SKIPPED') |
| details     | JSONB        |                                            |
| created_at  | TIMESTAMP    | NOT NUll, default timestamp                |

** Table Ingestion log

| Name          | Type        | Note                        |
| ------------- | ----------- | --------------------------- |
| id            | BIGINT      | Primary                     |
| source_type   | VARCHAR(50) | NOT NUll                    |
| status        | VARCHAR(30) | NOT NUll                    |
| total_records | INTEGER     | NOT NULL, default 0         |
| created_count | INTEGER     | NOT NULL, default 0         |
| skipped_count | INTEGER     | NOT NULL, default 0         |
| created_at    | TIMESTAMP   | NOT NUll, default timestamp |
