import sqlite3
from contextlib import contextmanager
from datetime import datetime

class Database:
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
        finally:
            conn.close()

    def get_all_tasks(self):
        """Fetch all tasks"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            return [dict(row) for row in cursor.fetchall()]

    def get_task_by_id(self, task_id):
        """Fetch a single task by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create_task(self, title):
        """Create a new task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
            conn.commit()
            return cursor.lastrowid

    def update_task(self, task_id, title=None, completed=None):
        """Update a task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if title is not None:
                updates.append('title = ?')
                params.append(title)
            if completed is not None:
                updates.append('completed = ?')
                params.append(completed)

            updates.append('updated_at = CURRENT_TIMESTAMP')
            params.append(task_id)

            if updates:
                query = f'UPDATE tasks SET {", ".join(updates)} WHERE id = ?'
                cursor.execute(query, params)
                conn.commit()

    def delete_task(self, task_id):
        """Delete a task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
