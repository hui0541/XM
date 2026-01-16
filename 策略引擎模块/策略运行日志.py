import time
import logging
import msgpack
import redis

class StrategyLogger:
    def __init__(self, strategy_id):
        self.strategy_id = strategy_id
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        
    def log(self, level, message):
        """
        通过 Redis 队列异步发送日志，避免写文件阻塞策略逻辑
        """
        log_entry = {
            'ts': int(time.time() * 1000),
            'sid': self.strategy_id,
            'lvl': level,
            'msg': message
        }
        # 推送到日志处理队列，由 Java 存储模块监听并落库
        self.r.lpush('system_logs_queue', msgpack.packb(log_entry))
        
        # 本地控制台打印输出
        print(f"[{level}][{self.strategy_id}] {message}")

    def info(self, msg): self.log('INFO', msg)
    def error(self, msg): self.log('ERROR', msg)