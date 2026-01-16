import redis
import msgpack
import time

class HighSpeedEngine:
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.market_safe = True  # 环境安全开关
        self.market_vibe = 1.0   # 环境加权系数

    def update_market_environment(self):
        """
        从 Redis 读取全局环境因子 (由行情适配层或中台计算)
        核心指标：
        1. sentiment_score: 0-100 (基于全市场涨跌家数比)
        2. index_slope: 指数5分钟斜率 (是否处于极速跳水期)
        """
        raw = self.r.get("global_market_env")
        if not raw:
            return
            
        env = msgpack.unpackb(raw, raw=False)
        
        # 因子 1: 市场赚钱效应。如果得分 < 30 (冰点)，停止开新仓
        sentiment_score = env.get('sentiment', 50)
        
        # 因子 2: 指数跳水保护。如果短时间内跌幅超过阈值，强制安全
        index_drop = env.get('index_drop', 0) 
        
        # 综合判定
        if sentiment_score < 30 or index_drop > 0.01:
            self.market_safe = False
        else:
            self.market_safe = True
            
        # 环境加权：环境好时加大仓位 (1.2)，环境一般时缩小仓位 (0.8)
        self.market_vibe = 1.2 if sentiment_score > 70 else 0.8

    def on_tick(self, packed_data):
        tick = msgpack.unpackb(packed_data, raw=False)
        
        # 每隔 1 秒更新一次环境因子，避免高频 tick 期间重复计算
        if int(time.time()) % 1 == 0:
            self.update_market_environment()

        # 环境因子过滤：如果大盘处于极端空头环境，即使个股信号出现也不下单
        if not self.market_safe:
            return 

        # 具体的个股策略逻辑
        if self.check_stock_alpha(tick):
            adjusted_qty = int(tick['base_qty'] * self.market_vibe)
            self.send_order(tick['code'], 'BUY', adjusted_qty)

    def check_stock_alpha(self, tick):
        # 你的个股因子逻辑（如 KDJ、均线等）
        return tick['price'] > tick['ma20']