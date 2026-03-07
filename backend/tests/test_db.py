from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.bfpklqcsulisroninusx:loppoc29min@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """))

    for row in result:
        print(row[0])