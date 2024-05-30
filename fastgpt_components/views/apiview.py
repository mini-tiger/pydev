from pydantic import BaseModel
import datetime

class DateExtractEntry(BaseModel):
    date: str



from datetime import datetime
async def date_extract_view(date_extract_entry: DateExtractEntry):

    print(date_extract_entry.date)
    # 输入字符串
    date_string = date_extract_entry.date

    # 使用字符串分割操作提取年、月、日、小时、分钟和秒
    date_parts = date_string.split(" ")
    date_parts_datetime = datetime.strptime(f"{date_parts[0]} {date_parts[1]}", "%Y-%m-%d %H:%M:%S")
    year = date_parts_datetime.year
    month = date_parts_datetime.month
    day = date_parts_datetime.day
    hour = date_parts_datetime.hour
    minute = date_parts_datetime.minute
    second = date_parts_datetime.second

    # # 输出结果
    # print("Year:", year)
    # print("Month:", month)
    # print("Day:", day)
    # print("Hour:", hour)
    # print("Minute:", minute)
    # print("Second:", second)

    return {"year": year, "month": month, "day": day, "hour": hour, "minute":minute, "second": second}
