import time

class FutureFunctionGuard:
    def __init__(self):
        self.last_processed_ts = 0

    def check_time_validity(self, tick_ts):
        """
        核心逻辑：
        1. 检查进入的时间戳是否单调递增。
        2. 确保策略无法获取当前处理时间戳之后的数据。
        """
        if tick_ts <= self.last_processed_ts:
            # 防止回测中数据乱序导致的未来函数欺骗
            return False
        
        real_now = time.time() * 1000
        if tick_ts > real_now + 1000: # 容忍1秒网络抖动
            print("警告：检测到疑似未来函数数据流入！")
            return False
            
        self.last_processed_ts = tick_ts
        return True