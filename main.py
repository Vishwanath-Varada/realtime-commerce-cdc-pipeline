import os
from decimal import Decimal
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from psycopg import Error as PsycopgError
from psycopg.conninfo import make_conninfo
from psycopg_pool import ConnectionPool


# ---------------------------------------------------------
# Load environment variables from .env
# ---------------------------------------------------------

load_dotenv()


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "realtime_commerce")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


if not POSTGRES_PASSWORD:
    raise RuntimeError(
        "POSTGRES_PASSWORD is missing. Add it to your .env file."
    )


# ---------------------------------------------------------
# PostgreSQL connection configuration
# ---------------------------------------------------------

DATABASE_URL = make_conninfo(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)


# ---------------------------------------------------------
# PostgreSQL Connection Pool
# ---------------------------------------------------------

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=5,
    max_size=30,
    timeout=10,
    open=False,
)


# ---------------------------------------------------------
# FastAPI startup / shutdown
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start PostgreSQL connection pool
    pool.open()

    # Wait until pool connections are ready
    pool.wait()

    print("PostgreSQL connection pool started")

    yield

    # Close pool when FastAPI shuts down
    pool.close()

    print("PostgreSQL connection pool closed")


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Real-Time Commerce API",
    description="Transaction API for the Real-Time Commerce CDC Pipeline",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# Transaction Request Model
# ---------------------------------------------------------

class Transaction(BaseModel):

    customer_id: int = Field(gt=0)

    product_id: int = Field(gt=0)

    quantity: int = Field(gt=0)

    amount: Decimal = Field(gt=0)


# ---------------------------------------------------------
# Home Endpoint
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Real-Time Commerce API is running"
    }


# ---------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    try:

        with pool.connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute("SELECT 1;")

                cursor.fetchone()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except PsycopgError as error:

        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {error}"
        )


# ---------------------------------------------------------
# Create Transaction Endpoint
# ---------------------------------------------------------

@app.post("/transactions")
def create_transaction(transaction: Transaction):

    try:

        # Borrow an existing connection from the pool
        with pool.connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO commerce.transactions
                    (
                        customer_id,
                        product_id,
                        quantity,
                        amount
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING transaction_id;
                    """,
                    (
                        transaction.customer_id,
                        transaction.product_id,
                        transaction.quantity,
                        transaction.amount,
                    )
                )

                result = cursor.fetchone()

                transaction_id = result[0]

            # Commit transaction to PostgreSQL
            conn.commit()

        return {
            "message": "Transaction saved to PostgreSQL",
            "transaction_id": transaction_id
        }

    except PsycopgError as error:

        raise HTTPException(
            status_code=500,
            detail=f"Database transaction failed: {error}"
        )