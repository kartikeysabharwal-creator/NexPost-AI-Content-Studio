import sqlite3
import os
import json
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexpost.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS post_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        topic TEXT NOT NULL,
        length TEXT NOT NULL,
        language TEXT NOT NULL,
        tone TEXT NOT NULL,
        variation_type TEXT NOT NULL,
        post_content TEXT NOT NULL,
        model_name TEXT NOT NULL,
        quality_score INTEGER NOT NULL,
        hook_score INTEGER NOT NULL,
        readability_score INTEGER NOT NULL,
        cta_score INTEGER NOT NULL,
        word_count INTEGER NOT NULL,
        read_time_seconds INTEGER NOT NULL,
        latency_seconds REAL NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rewrite_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        goal TEXT NOT NULL,
        original_text TEXT NOT NULL,
        rewritten_text TEXT NOT NULL,
        model_name TEXT NOT NULL,
        latency_seconds REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_post(topic, length, language, tone, variation_type, post_content, model_name, metrics):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO post_history (
        timestamp, topic, length, language, tone, variation_type,
        post_content, model_name, quality_score, hook_score,
        readability_score, cta_score, word_count, read_time_seconds, latency_seconds
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        topic,
        length,
        language,
        tone,
        variation_type,
        post_content,
        model_name,
        metrics.get("overall_score", 85),
        metrics.get("hook_score", 85),
        metrics.get("readability_score", 85),
        metrics.get("cta_score", 85),
        metrics.get("words", 0),
        metrics.get("read_time_seconds", 10),
        metrics.get("latency", 0.8)
    ))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def save_rewrite(goal, original_text, rewritten_text, model_name, latency):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO rewrite_history (
        timestamp, goal, original_text, rewritten_text, model_name, latency_seconds
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        goal,
        original_text,
        rewritten_text,
        model_name,
        latency
    ))
    conn.commit()
    conn.close()

def get_all_posts(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_history_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(quality_score), AVG(latency_seconds) FROM post_history")
    row = cursor.fetchone()
    conn.close()
    count = row[0] if row else 0
    avg_quality = round(row[1], 1) if row and row[1] else 0.0
    avg_latency = round(row[2], 2) if row and row[2] else 0.0
    return {"total_posts": count, "avg_quality": avg_quality, "avg_latency": avg_latency}

# Initialize tables immediately
init_db()
