# -*- coding: utf-8 -*-
import redis
import msgpack
import time
import logging
import json
from threading import Thread

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HighSpeedEngine:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        # 使用连接池管理 Redis 连接，提升多线程下的性能
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, decode_responses=False)
        self.r = redis.StrictRedis(connection_pool=self.pool)
        self.running = False
        self.strategy_channel = "market_tick_channel" # 订阅行情的频道
        self.order_queue = "order_submission_queue"   # 发送订单的队列

    def process_market_tick(self, message):
        """
        处理单条行情数据，这是策略逻辑的核心入口
        """
        try:
            # 假设 C++ 写入的是 msgpack 二进制流，解包速度快
            tick_data = msgpack.unpackb(message['data'], raw=False)
            
            # --- 策略逻辑区域 ---
            # 示例：简单的双均线或突破策略
            symbol = tick_data.get('symbol')
            price = tick_data.get('last_price')
            
            if price and price > 100000: # 示例触发条件
                self.send_order(symbol, 'BUY', price, 1.0)
            # ---------------------

        except Exception as e:
            logger.error(f"Error processing tick: {e}")

    def send_order(self, symbol, direction, price, volume):
        """
        发送订单到执行模块 (Java)
        """
        order_packet = {
            'id': str(time.time()), # 简易ID，生产环境需用 UUID 或雪花算法
            'symbol': symbol,
            'direction': direction,
            'price': price,
            'volume': volume,
            'timestamp': time.time()
        }
        
        try:
            # 使用 msgpack 序列化订单，比 JSON 更小更快
            packed_order = msgpack.packb(order_packet)
            # 推送到 Redis 队列，Java 端通过 BLPOP 消费
            self.r.lpush(self.order_queue, packed_order)
            logger.info(f"Order sent: {symbol} {direction} @ {price}")
        except redis.RedisError as e:
            logger.critical(f"Redis error sending order: {e}")

    def start(self):
        """
        启动引擎，使用 Pub/Sub 模式监听行情
        """
        self.running = True
        logger.info("Strategy Engine Started. Waiting for data...")
        
        pubsub = self.r.pubsub()
        pubsub.subscribe(**{self.strategy_channel: self.process_market_tick})

        # 主循环
        try:
            thread = pubsub.run_in_thread(sleep_time=0.001)
            # 保持主线程活跃
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            thread.stop()

    def stop(self):
        self.running = False
        logger.info("Strategy Engine Stopped.")

if __name__ == "__main__":
    engine = HighSpeedEngine()
    engine.start()