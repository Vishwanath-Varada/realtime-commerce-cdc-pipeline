\# ⚡ Real-Time Commerce CDC Pipeline



\### PostgreSQL → Debezium → Apache Kafka → Snowflake



A production-style \*\*real-time Change Data Capture (CDC) pipeline\*\* that captures transactional changes from PostgreSQL, streams them through Debezium and Apache Kafka, and delivers analytics-ready data into Snowflake using \*\*RAW, Silver, and Gold layers\*\*.



The project includes a FastAPI transaction service, PostgreSQL connection pooling, automated CDC processing, Snowflake Streams \& Tasks, business analytics, and high-concurrency load testing with Locust.



\---



\## 🚀 Project Highlights



\- ⚡ Real-time PostgreSQL WAL-based CDC

\- 🔄 Debezium change-event capture

\- 📡 Apache Kafka event streaming

\- ❄️ Snowflake Kafka Sink integration

\- 🥉 RAW → 🥈 Silver → 🥇 Gold architecture

\- 🔁 Automated Snowflake Stream + Task + MERGE processing

\- 🧩 INSERT, UPDATE, DELETE, and snapshot CDC support

\- 🚀 FastAPI transaction ingestion API

\- 🔗 PostgreSQL connection pooling

\- 📊 Business-ready Gold analytics

\- 🧪 Locust performance and concurrency testing

\- ✅ End-to-end PostgreSQL → Snowflake reconciliation



\---



\# 🏗️ Architecture



```text

&#x20;                        ┌─────────────────┐

&#x20;                        │     LOCUST      │

&#x20;                        │   Load Testing  │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │     FastAPI     │

&#x20;                        │ Transaction API │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │   PostgreSQL    │

&#x20;                        │  OLTP Database  │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 │ WAL

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │    Debezium     │

&#x20;                        │      CDC        │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │  Apache Kafka   │

&#x20;                        │  Event Stream   │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │    Snowflake    │

&#x20;                        │    RAW Layer    │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                        Stream + Task + MERGE

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │  SILVER Layer   │

&#x20;                        │  Current State  │

&#x20;                        └────────┬────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌─────────────────┐

&#x20;                        │   GOLD Layer    │

&#x20;                        │    Analytics    │

&#x20;                        └─────────────────┘

```



\---



\# 🧰 Technology Stack



| Layer | Technology |

|---|---|

| API | FastAPI, Python |

| Transaction Database | PostgreSQL |

| Connection Management | Psycopg Connection Pool |

| CDC | Debezium |

| Event Streaming | Apache Kafka |

| Connector Runtime | Kafka Connect |

| Data Warehouse | Snowflake |

| Incremental Processing | Snowflake Streams |

| Automation | Snowflake Tasks |

| Data Synchronization | SQL MERGE |

| Analytics Architecture | RAW / Silver / Gold |

| Load Testing | Locust |

| Containerization | Docker Compose |



\---



\# 🔄 Change Data Capture Flow



PostgreSQL writes every committed database change to its \*\*Write-Ahead Log (WAL)\*\*.



Debezium continuously reads those changes and converts them into CDC events.



```text

PostgreSQL Transaction

&#x20;       ↓

PostgreSQL WAL

&#x20;       ↓

Debezium

&#x20;       ↓

Kafka Topic

&#x20;       ↓

Snowflake RAW

&#x20;       ↓

Stream

&#x20;       ↓

Task

&#x20;       ↓

MERGE

&#x20;       ↓

Silver Current State

```



\### CDC Operations Validated



| Debezium Operation | Meaning | Silver Action | Result |

|---|---|---|---|

| `r` | Snapshot Read | Insert current record | ✅ |

| `c` | Create | Insert | ✅ |

| `u` | Update | Update existing record | ✅ |

| `d` | Delete | Delete current record | ✅ |



\---



\# 🥉 RAW Layer



The RAW layer preserves incoming CDC events from Kafka.



```text

REALTIME\_COMMERCE\_DB.RAW.TRANSACTIONS\_RAW

```



Primary fields include:



```text

RECORD\_METADATA

RECORD\_CONTENT

```



The RAW layer retains CDC event history rather than representing only the latest database state.



\---



\# 🥈 Silver Layer



The Silver layer maintains the \*\*current version of every transaction\*\*.



```text

REALTIME\_COMMERCE\_DB.SILVER.TRANSACTIONS\_CURRENT

```



Processing is automated using:



```text

RAW.TRANSACTIONS\_RAW

&#x20;       ↓

TRANSACTIONS\_RAW\_STREAM

&#x20;       ↓

TRANSACTIONS\_CDC\_TASK

&#x20;       ↓

MERGE

&#x20;       ↓

SILVER.TRANSACTIONS\_CURRENT

```



The MERGE logic handles:



\- New records

\- Updated records

\- Deleted records

\- Snapshot records

\- Deduplication of multiple CDC events



\---



\# 🥇 Gold Analytics Layer



The Gold layer exposes business-ready analytical views.



\### 📊 Transaction Summary



```text

GOLD.TRANSACTION\_SUMMARY

```



Provides:



\- Total transactions

\- Total customers

\- Total products

\- Total revenue

\- Average transaction value

\- Total units sold



\### 📅 Daily Sales



```text

GOLD.DAILY\_SALES

```



Provides:



\- Daily transaction volume

\- Daily revenue

\- Unique customers

\- Units sold

\- Average transaction value



\### 📦 Top Products



```text

GOLD.TOP\_PRODUCTS

```



Provides:



\- Transactions by product

\- Units sold

\- Revenue by product

\- Average transaction value



\### 👥 Customer Analytics



```text

GOLD.CUSTOMER\_ANALYTICS

```



Provides:



\- Customer transaction count

\- Total units purchased

\- Lifetime spend

\- Average transaction value

\- First transaction

\- Most recent transaction



\---



\# 🚀 Performance Benchmark



\## 500 Concurrent User Load Test



The FastAPI transaction API was load-tested locally using \*\*Locust\*\*.



\### Test Configuration



| Configuration | Value |

|---|---:|

| Concurrent simulated users | \*\*500\*\* |

| Spawn rate | \*\*50 users/sec\*\* |

| Endpoint | `POST /transactions` |



\### Results



| Metric | Result |

|---|---:|

| Total API requests | \*\*505,847\*\* |

| Failed requests | \*\*0\*\* |

| Failure rate | \*\*0%\*\* |

| Throughput | \*\*\~590.1 RPS\*\* |

| Average response time | \*\*\~727 ms\*\* |

| Median response time | \*\*\~720 ms\*\* |

| p95 response time | \*\*\~920 ms\*\* |

| p99 response time | \*\*\~1.0 sec\*\* |

| Maximum response time | \*\*\~3.0 sec\*\* |



> These results were measured in a local development environment using simulated Locust users and represent project benchmark results rather than production capacity guarantees.



\---



\# ✅ End-to-End Data Reconciliation



After the 500-user load test, the operational PostgreSQL database and Snowflake Silver layer were compared.



| System | Final Row Count |

|---|---:|

| PostgreSQL | \*\*671,891\*\* |

| Snowflake Silver | \*\*671,891\*\* |

| Difference | \*\*0\*\* |



```text

PostgreSQL       671,891

Snowflake Silver 671,891

&#x20;                ───────

Difference             0

```



\### Result



✅ Source and destination reconciled exactly.



This validated the complete pipeline:



```text

FastAPI

&#x20;  ↓

PostgreSQL

&#x20;  ↓

Debezium

&#x20;  ↓

Kafka

&#x20;  ↓

Snowflake RAW

&#x20;  ↓

Silver

```



under sustained concurrent traffic.



\---



\# 📸 Load Test Evidence



\## Locust — 500 Concurrent Users / 500K+ Requests



!\[Locust 500 User Load Test](./docs/images/locust-500-users-500k.png)



\---



\## PostgreSQL Final Row Count



!\[PostgreSQL Reconciliation](./docs/images/postgresql-671891-rows.png)



\---



\## Snowflake Silver Final Row Count



!\[Snowflake Silver Reconciliation](./docs/images/snowflake-silver-671891-rows.png)



\---



\# ⚙️ Performance Optimization



During initial testing, the API opened a new PostgreSQL connection for every request.



That design became a major performance bottleneck under concurrency.



\### Before Optimization



```text

HTTP Request

&#x20;    ↓

Create PostgreSQL Connection

&#x20;    ↓

Execute INSERT

&#x20;    ↓

Commit

&#x20;    ↓

Close Connection

```



\### Optimized Architecture



The API was upgraded to use a reusable PostgreSQL connection pool.



```text

&#x20;                   ┌── DB Connection

&#x20;                   │

FastAPI → Connection Pool ── DB Connection

&#x20;                   │

&#x20;                   └── DB Connection

```



This dramatically reduced connection overhead and improved throughput under concurrent traffic.



\---



\# 🧪 Reliability Testing



The project validated the complete CDC lifecycle.



```text

CREATE  ✅

UPDATE  ✅

DELETE  ✅

SNAPSHOT ✅

```



Example:



```text

PostgreSQL UPDATE

&#x20;      ↓

WAL

&#x20;      ↓

Debezium

&#x20;      ↓

Kafka

&#x20;      ↓

Snowflake RAW

&#x20;      ↓

Stream + Task

&#x20;      ↓

MERGE

&#x20;      ↓

Silver record automatically updated

```



\---



\# 📁 Repository Structure



```text

realtime-commerce-cdc-pipeline/

│

├── main.py

├── locustfile.py

├── docker-compose.yml

├── requirements.txt

├── .env.example

├── .gitignore

├── README.md

│

├── sql/

│   ├── snowflake\_setup.sql

│   ├── silver\_initial\_load.sql

│   ├── silver\_cdc\_merge.sql

│   └── gold\_analytics.sql

│

└── docs/

&#x20;   └── images/

&#x20;       ├── locust-500-users-500k.png

&#x20;       ├── postgresql-671891-rows.png

&#x20;       └── snowflake-silver-671891-rows.png

```



\---



\# 🔐 Security



Sensitive information is excluded from source control.



The repository does \*\*not\*\* include:



```text

.env

PostgreSQL passwords

Snowflake private keys

Snowflake public-key files

Python virtual environments

Downloaded connector binaries

```



Developers can configure their environment using:



```text

.env.example

```



\---



\# ▶️ Running the Project



\### 1. Clone the repository



```bash

git clone <repository-url>

```



\### 2. Create a Python environment



```bash

python -m venv venv

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create:



```text

.env

```



using:



```text

.env.example

```



as the template.



\### 5. Start Kafka and Kafka Connect



```bash

docker compose up -d

```



\### 6. Start FastAPI



```bash

uvicorn main:app --host 127.0.0.1 --port 8000

```



\### 7. Open FastAPI Swagger



```text

http://127.0.0.1:8000/docs

```



\---



\# 💡 Engineering Concepts Demonstrated



\- Change Data Capture

\- PostgreSQL Write-Ahead Logging

\- Event-driven architecture

\- Apache Kafka

\- Kafka Connect

\- Debezium

\- Snowflake ingestion

\- Incremental data processing

\- Snowflake Streams

\- Snowflake Tasks

\- SQL MERGE

\- Medallion architecture

\- Data reconciliation

\- Connection pooling

\- REST API development

\- Load testing

\- Performance tuning

\- High-concurrency transaction processing



\---



\# 🎯 Benchmark Summary



```text

500 Concurrent Simulated Users

505,847 API Requests

0 Failed Requests

\~590 Requests/Second

671,891 PostgreSQL Rows

671,891 Snowflake Silver Rows

0 Row Difference

```



\---



\## 👨‍💻 Author



\### Vishwanath Varada



\*\*Data Engineering • Real-Time Data Pipelines • Python • SQL • Apache Kafka • Snowflake\*\*

