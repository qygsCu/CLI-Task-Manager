import sqlite3


# 规范1：把数据库文件名定义为全局大写常量，方便以后统一修改
DB_FILE = 'taskmaster.db'

def init_db():
    """
    规范2：初始化函数。
    程序第一次运行时调用，负责创建表。
    核心SQL思路：CREATE TABLE IF NOT EXISTS tasks (...)
    需要包含的字段：id (主键，自增), title (文本), is_done (布尔/整数), created_at (时间戳)
    """
    # 你的任务：查文档，看看如何用 sqlite3 连接 DB_FILE 并执行 CREATE TABLE 语句
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    create_table_sql = """CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        is_done INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)"""
    cur.execute(create_table_sql)
    con.commit()
    con.close()


def add_task(title: str):
    """
    规范3：增加数据。
    核心SQL思路：INSERT INTO tasks (title, is_done) VALUES (?, ?)
    注意：执行完 INSERT、UPDATE、DELETE 后，必须调用 conn.commit() 保存更改！
    """
    # 你的任务：实现插入逻辑


def get_all_tasks() -> list:
    """
    规范4：查询数据。
    核心SQL思路：SELECT id, title, is_done FROM tasks
    注意：查询操作不需要 commit()，只需要 fetchall() 把数据拉回来。
    """
    pass # 你的任务：实现查询并返回结果

if __name__ == "__main__":
    init_db()
    print("数据库初始化成功")