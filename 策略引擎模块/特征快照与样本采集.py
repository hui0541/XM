import pandas as pd
import numpy as np
import os
import datetime

class FeatureCollector:
    """
    特征采集器
    职责：在交易时刻快照当前因子值，用于后续机器学习模型训练
    """
    def __init__(self, save_dir="./samples"):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.save_dir = save_dir
        self.buffer = []

    def snapshot(self, symbol, timestamp, factors: dict, action):
        """
        快照一次决策现场
        :param factors: 当前计算好的因子值 (如 RSI, MACD, OrderImbalance)
        :param action: 策略采取的动作 (Buy/Sell/Hold)
        """
        record = {
            "symbol": symbol,
            "timestamp": timestamp,
            "action": action,
            **factors # 展开因子
        }
        self.buffer.append(record)
        
        # 内存中积攒一定数量后落盘 (Parquet格式效率最高)
        if len(self.buffer) >= 1000:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
            
        df = pd.DataFrame(self.buffer)
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(self.save_dir, f"features_{date_str}.parquet")
        
        # Append 模式需要特定引擎支持，这里简化为追加多个文件
        # 实际生产建议写入 ClickHouse，这里演示写入文件
        timestamp_ns = int(datetime.datetime.now().timestamp() * 1e6)
        unique_path = os.path.join(self.save_dir, f"feat_{date_str}_{timestamp_ns}.csv")
        
        df.to_csv(unique_path, index=False)
        self.buffer.clear()
        print(f"[SampleCollector] 样本已落盘: {unique_path}")