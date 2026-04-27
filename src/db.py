import sqlite3

# データベースファイルの名前（プロジェクト直下に作成されます）
DB_FILE = "todo.db"

def get_db():
    """データベース接続を作成して返す"""
    conn = sqlite3.connect(DB_FILE)
    # 辞書のようにカラム名（id, title等）でデータにアクセスできるようにする設定
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """テーブルが存在しなければ作成する（手動作成の自動化）"""
    conn = get_db()
    cursor = conn.cursor()
    # TODOテーブルの作成。SQLiteではBOOLEANは内部的に0か1の整数として扱われます。
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()