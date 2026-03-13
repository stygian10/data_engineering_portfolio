from sqlalchemy import create_engine, text  # note the text import

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "weather_db"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    with engine.connect() as conn:
        # Wrap raw SQL string with text()
        result = conn.execute(text("SELECT version();"))
        print("✅ Connected successfully to PostgreSQL:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
