import time
from datetime import datetime
from functools import wraps

class FutureDataError(Exception):
    """当策略试图访问未来数据时抛出"""
    pass

class TimeMachineProxy:
    """
    数据访问代理（时光机）
    职责：拦截所有对数据的读取操作，核对时间戳
    """
    def __init__(self, data_source, current_time_func):
        self._data = data_source
        self._get_current_time = current_time_func

    def __getitem__(self, key):
        # 假设 key 是时间戳或索引
        # 这里仅做逻辑演示，实际需根据 pandas/numpy 的索引类型适配
        requested_time = self._parse_time(key)
        current_time = self._get_current_time()

        if requested_time > current_time:
            raise FutureDataError(
                f"未来函数违规! 当前时间: {current_time}, 试图访问: {requested_time}"
            )
        
        return self._data[key]

    def _parse_time(self, key):
        # 简化处理：假设 key 本身就是时间戳
        return key

    def __getattr__(self, name):
        # 代理其他属性访问
        return getattr(self._data, name)

def strict_timing(func):
    """
    装饰器：强制执行时间检查
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 在这里可以注入一些运行时检查逻辑
        return func(*args, **kwargs)
    return wrapper

# ----------------------------------------------------
# 单元测试 / 使用示例
# ----------------------------------------------------
if __name__ == "__main__":
    # 模拟环境
    simulated_now = 100
    
    data = {90: "过去", 100: "现在", 110: "未来"}
    
    # 包装
    safe_data = TimeMachineProxy(data, lambda: simulated_now)
    
    try:
        print(f"访问过去: {safe_data[90]}") # OK
        print(f"访问未来: {safe_data[110]}") # 报错
    except FutureDataError as e:
        print(f"捕获违规: {e}")