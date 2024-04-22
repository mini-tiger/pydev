import webapi.config as config
import threading
from webapi.log.setup import logger
import time, sqlite3

# 创建和初始化数据库
db_path = 'database.db'
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
# 删除已存在的 ip_pool 表
cursor.execute('DROP TABLE IF EXISTS ip_pool')

cursor.execute('''
    CREATE TABLE ip_pool (
        ip TEXT PRIMARY KEY,
        in_use BOOLEAN,
        start_time REAL
    )
''')
conn.commit()


class IPPool:
    def __init__(self, ip_list, msg, timeout=3600):
        self.msg = msg
        self.timeout = timeout
        with conn:
            conn.executemany('insert or ignore INTO ip_pool (ip, in_use, start_time) VALUES (?, ?, ?)',
                             [(ip, False, None) for ip in ip_list])

        # 启动超时和监控线程
        if "global" in msg.lower():
            self.timeout_thread = threading.Thread(target=self.release_timeout_ips)
            self.timeout_thread.daemon = True
            self.timeout_thread.start()

            self.monitor_thread = threading.Thread(target=self.monitor_ip_usage)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

    def acquire_ip(self):
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ip FROM ip_pool WHERE in_use = FALSE LIMIT 1')
            result = cursor.fetchone()
            if result:
                ip = result[0]
                cursor.execute('UPDATE ip_pool SET in_use = TRUE, start_time = ? WHERE ip = ?', (time.time(), ip))
                conn.commit()
                cursor.close()
                logger.warning(f"IP acquired: {ip}")

                return ip
            else:
                logger.warning("No available IP.")
                return None

    def release_ip(self, ip):

        cursor = conn.cursor()
        cursor.execute('UPDATE ip_pool SET in_use = FALSE, start_time = NULL WHERE ip = ?', (ip,))
        conn.commit()
        cursor.close()
        logger.warning(f"IP released: {ip}")

    def release_timeout_ips(self):
        while True:
            current_time = time.time()
            cursor = conn.cursor()
            conn.execute('''
                UPDATE ip_pool SET in_use = FALSE, start_time = NULL
                WHERE in_use = TRUE AND (? - start_time) > ?
            ''', (current_time, self.timeout))
            conn.commit()
            cursor.close()
            time.sleep(min(self.timeout / 10, 60))

    def monitor_ip_usage(self):
        while True:
            used_ips, total_ips = self.get_available_ips_count()
            logger.warning(f"IP Pool Usage: used: {','.join(used_ips)} ;total:  {','.join(total_ips)} IPs in use.")
            time.sleep(30)

    def get_available_ips_count(self):
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT ip FROM ip_pool WHERE in_use = TRUE')
            used_ips = [row[0] for row in cursor.fetchall()]
            cursor.execute('SELECT ip FROM ip_pool')
            total_ips = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return used_ips, total_ips
        except Exception as e:
            logger.error(f"get_available_ips_count Exception: {e}")
            return [],[]

    def get_available_ips(self):
        try:
            used_ips, total_ips = self.get_available_ips_count()

            return len(total_ips) - len(used_ips) >= 1
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return False


global_api_pool = IPPool(ip_list=config.BaseConfig.OPENAI_API_BASE_LIST, msg="Global API pool")
