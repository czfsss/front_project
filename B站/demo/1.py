query = "start-date: undefined\nend-date: undefined\nmch_name: undefined\nclassgroup: undefined\nclasslabel: 白班"


from datetime import datetime

def format_gmt_date(gmt_string):
    """将GMT格式的时间字符串转换为YYYY-MM-DD格式"""
    try:
        dt = datetime.strptime(gmt_string, "%a, %d %b %Y %H:%M:%S GMT")
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return gmt_string  # 如果转换失败，返回原字符串

def main(query: str) -> dict:
    # 处理输入字符串
    query_lists = query.split("\n")
    query_dict = {}
    for item in query_lists:
        key, value = item.split(": ")
        if value == "undefined":
            value = ""
        query_dict[key] = value
    
    # 处理时间参数
    start_date = query_dict.get("start-date", "")
    end_date = query_dict.get("end-date", "")
    
    # 转换时间格式（如果是GMT格式）
    if start_date and "GMT" in start_date:
        start_date = format_gmt_date(start_date)
    if end_date and "GMT" in end_date:
        end_date = format_gmt_date(end_date)
    
    # 校验结束日期不能小于开始日期
    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            if end_dt < start_dt:
                return {
                    "status": "error",
                    "message": "结束日期不能小于开始日期",
                    "start_date": start_date,
                    "end_date": end_date,
                    "mch_name": query_dict.get("mch_name", ""),
                    "classgroup": query_dict.get("classgroup", ""),
                    "classlabel": query_dict.get("classlabel", ""),
                }
        except ValueError:
            # 如果日期格式不正确，继续执行不进行校验
            pass
    
    return {
        "status": "success",
        "message": "筛选条件合格",
        "start_date": start_date,
        "end_date": end_date,
        "mch_name": query_dict.get("mch_name", ""),
        "classgroup": query_dict.get("classgroup", ""),
        "classlabel": query_dict.get("classlabel", ""),
    }


if __name__ == "__main__":
    print(main(query))
