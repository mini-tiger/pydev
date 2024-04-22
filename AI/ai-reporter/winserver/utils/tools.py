from datetime import datetime, timezone, timedelta



def get_current_unix():
    # 获取当前时间
    current_time = datetime.now()

    # 计算中国时区的偏移量
    china_timezone_offset = timedelta(hours=8)  # 中国时区为UTC+8

    # 将当前时间加上中国时区的偏移量，即得到中国时间
    china_current_time = current_time + china_timezone_offset

    # 将中国时间转换为时间戳
    return int(china_current_time.timestamp())