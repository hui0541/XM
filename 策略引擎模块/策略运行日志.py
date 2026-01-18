import time
import logging
import os
import json
from threading import Thread
from queue import Queue

class StrategyLogger:
    """
    高性能异步日志记录器
    职责：记录策略决策路径、耗时、异常，用于盘后复盘
    """
    def __init__(self, log_dir="../一键启动器模块/logs", strategy_name="DemoStrategy"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        self.strategy_name = strategy_name
        self.log_file = os.path.join(log_dir, f"strategy_{strategy_name}.jsonl")
        self.queue = Queue()
        self.running = True
        
        # 启动后台写入线程
        self.writer_thread = Thread(target=self._worker, daemon=True)
        self.writer_thread.start()

    def log_execution(self, event_type, tick_time, process_ns, decision_info):
        """
        记录一次执行上下文
        :param event_type: 'on_tick' | 'on_bar'
        :param tick_time: 行情发生时间
        :param process_ns: 策略计算耗时(纳秒)
        :param decision_info: 决策结果 (dict)
        """
        entry = {
            "ts": time.time(),
            "algo": self.strategy_name,
            "event": event_type,
            "tick_t": tick_time,
            "cost_us": process_ns / 1000.0, # 微秒
            "data": decision_info
        }
        self.queue.put(entry)

    def _worker(self):
        """ 后台线程：批量写入文件 """
        buffer = []
        while self.running or not self.queue.empty():
            try:
                # 阻塞获取，带超时以便定期 flush
                item = self.queue.get(timeout=1)
                buffer.append(json.dumps(item))
                
                # 批量写入 (每100条或超时)
                if len(buffer) >= 100:
                    self._flush(buffer)
            except:
                if buffer:
                    self._flush(buffer)
        if buffer:
            self._flush(buffer)
    
    def _flush(self, buffer):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("\n".join(buffer) + "\n")
        buffer.clear()

    def close(self):
        self.running = False
        self.writer_thread.join()
