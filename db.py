import sqlite3
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
    cur.close()
    con.close()


def add_task(title: str):
    """
    规范3：增加数据。
    核心SQL思路：INSERT INTO tasks (title, is_done) VALUES (?, ?)
    注意：执行完 INSERT、UPDATE、DELETE 后，必须调用 conn.commit() 保存更改！
    """
    # 你的任务：实现插入逻辑
    existed_titles = get_all_notdone_titles()
    if (title, ) in existed_titles:
        print("该任务已存在！")
        return 
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    data = (title, )
    add_task_sql = """INSERT INTO tasks (title) VALUES (?)"""
    cur.execute(add_task_sql, data)
    con.commit()
    cur.close()
    con.close()

def delete_all_tasks():
    """
    删除所有任务
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    delete_all_tasks_sql = """DELETE FROM tasks"""
    cur.execute(delete_all_tasks_sql)
    con.commit()
    cur.close()
    con.close()

def get_all_tasks() -> list:
    """
    规范4：查询数据。
    核心SQL思路：SELECT id, title, is_done FROM tasks
    注意：查询操作不需要 commit()，只需要 fetchall() 把数据拉回来。
    """
    # 你的任务：实现查询并返回结果
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    get_all_tasks_sql = """SELECT id, title, is_done FROM tasks"""
    cur.execute(get_all_tasks_sql)
    res = cur.fetchall()
    cur.close()
    con.close()
    return res

def get_all_notdone_titles() -> list:
    """
    返回所有未完成的任务的title
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    get_all_notdone_titles_sql= """SELECT title FROM tasks WHERE is_done = 0"""
    cur.execute(get_all_notdone_titles_sql)
    res = cur.fetchall()
    cur.close()
    con.close()
    return res
    
def delete_task(title: str):
    """
    根据任务title删除任务
    """
    existed_titles = get_all_notdone_titles()
    existed_titles = [i[1] for i in existed_titles]
    if title not in existed_titles:
        print("该任务不在待办任务中！")
        res = process.extractOne(title, existed_titles)
        if (res[1] >= 75):
            print(f"你是否在找：{res[0][0]}")
        return 
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    delete_task_sql = f"""DELETE FROM tasks WHERE title = ?"""
    cur.execute(delete_task_sql, (title, ))
    con.commit()
    cur.close()
    con.close()

def mark_task_done(title: str):
    """
    将任务标记为完成
    """
    existed_titles = get_all_notdone_titles()
    if (title, ) not in existed_titles:
        all_titles = get_all_tasks()
        all_titles = [x[1] for x in all_titles]
        if title not in all_titles:
            print("该任务不存在！")
            res = process.extractOne(title, existed_titles)
            if (res[1] >= 10):
                print(f"你是否在找：{res[0][0]}")
        else:
            print("该任务已完成！")
        return 
    else:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        mark_task_done_sql = f"""UPDATE tasks SET is_done = 1 WHERE title = ?"""
        cur.execute(mark_task_done_sql, (title, ))
        con.commit()
        cur.close()
        con.close()
        


if __name__ == "__main__":
    mark_task_done("写作业哈哈哈哈哈哈哈啊哈")
    pass
    