import pymysql

# 建立连接，所有操作都放在这个 with 块内
with pymysql.connect(
    host='localhost',
    user='root',
    password='xwc1186256858',
    database='kdtx',
    charset='utf8mb4'
) as connection:

    # 准备数据
    users = [
        ('dola', 'pass123'),
        ('qwer', 'qwerty'),
        ('charlse', '123456'),
    ]

    # 创建游标
    with connection.cursor() as cursor:

        # 1. 批量插入
        cursor.executemany(
            "INSERT INTO user (username, password) VALUES (%s, %s)",
            users
        )
        inserted = cursor.rowcount

        # 2. 更新（假设 alice 存在）
        cursor.execute(
            "UPDATE user SET password = %s WHERE username = %s",
            ('newpassword', 'alice')
        )
        updated = cursor.rowcount

        # 3. 删除（假设 bob 存在）
        cursor.execute(
            "DELETE FROM user WHERE username = %s",
            ('bob',)
        )
        deleted = cursor.rowcount

        # 4. 查询
        cursor.execute(
            "SELECT id, username, password FROM user WHERE password LIKE %s",
            ('123%',)
        )
        rows = cursor.fetchall()

        # 所有操作成功后，统一提交
        connection.commit()

        # 输出结果
        print(f"插入了 {inserted} 行")
        print(f"更新了 {updated} 行")
        print(f"删除了 {deleted} 行")
        print("查询结果：")
        for row in rows:
            print(row)