"""
Database & RLS Verification Script
Checks tables, indexes, and Row Level Security policies on Supabase Managed PostgreSQL
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL")

conn = psycopg2.connect(DATABASE_SYNC_URL)
cursor = conn.cursor()

print("--- 1. Checking Core Multi-Tenant Tables ---")
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
""")
tables = [row[0] for row in cursor.fetchall()]
for t in tables:
    print(f"  [TABLE] {t}")

print("\n--- 2. Checking Row Level Security (RLS) Status & Policies ---")
cursor.execute("""
    SELECT 
        c.relname AS table_name,
        c.relrowsecurity AS rls_enabled,
        pol.polname AS policy_name,
        pol.polqual AS policy_expression
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    LEFT JOIN pg_policy pol ON pol.polrelid = c.oid
    WHERE n.nspname = 'public' AND c.relkind = 'r'
    ORDER BY c.relname;
""")
rls_info = cursor.fetchall()
for row in rls_info:
    table_name, rls_enabled, pol_name, pol_expr = row
    status = "ENABLED" if rls_enabled else "DISABLED"
    print(f"  [RLS] Table '{table_name}': {status} | Policy: {pol_name}")

conn.close()
print("\n--- DB Verification Complete ---")
