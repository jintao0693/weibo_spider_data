import pymysql
from datetime import datetime

# 假设 process_time 函数已经定义
def process_time(publish_time):
    # 示例处理逻辑，根据实际需求修改
    return datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')

def process_event_list(event_list):
    for event in event_list:
        event['personal_href'] = 'https:' + event['personal_href']
        event['publish_time'] = process_time(event['publish_time'])
    return event_list

def save_to_database(event_list):
    # 数据库连接配置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456789',
        'database': 'one_data',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    # 连接到 MySQL 数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 批量插入数据
    insert_query = '''
        INSERT INTO events (mid, uid, title, nickname, personal_href, event_source, content_show, publish_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    # 准备插入的数据
    data_to_insert = [
        (
            event['mid'],
            event['uid'],
            event['title'],
            event['nike_name'],
            event['personal_href'],
            event['event_source'],
            event['content_show'],
            event['publish_time']
        )
        for event in event_list
    ]

    # 执行批量插入
    cursor.executemany(insert_query, data_to_insert)

    # 提交事务
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()
    print("数据已成功保存到数据库！")