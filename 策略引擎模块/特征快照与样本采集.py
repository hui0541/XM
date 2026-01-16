class FeatureCollector:
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost')

    def capture_with_env(self, tick, stock_features):
        """
        将个股特征与市场环境特征拼合
        """
        # 获取当前全局环境
        env_raw = self.r.get("global_market_env")
        env_data = msgpack.unpackb(env_raw) if env_raw else {}
        
        # 特征拼接：[个股因子1, 个股因子2, ..., 市场情绪得分, 市场波动率]
        combined_features = stock_features + [
            env_data.get('sentiment', 50),
            env_data.get('volatility', 0)
        ]
        
        sample = {
            'ts': tick['ts'],
            'code': tick['code'],
            'X': combined_features,
            'y': 0 # 待后续打标
        }
        self.r.lpush('ai_training_samples', msgpack.packb(sample))