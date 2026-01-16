import socket
import struct
import time
import sys
import signal
from collections import deque

# 引入兄弟模块
from 策略运行日志 import StrategyLogger
from 特征快照与样本采集 import FeatureCollector

# ==========================================
# 配置区域
# ==========================================
UDP_IP = "0.0.0.0"
UDP_PORT = 9999
BUFFER_SIZE = 1024 # 足够容纳 256 bytes 的 TickData

# C++ TickData 结构体布局 (Alignas 64)
# char symbol[16];      -> 16s
# int64 timestamp;      -> q
# int64 local_time;     -> q
# int64 last_price;     -> q (需 / 10000.0)
# int64 volume;         -> q
# int64 turnover;       -> q
# int64 open_interest;  -> q
# int64 bid_price[5];   -> 5q
# int64 bid_volume[5];  -> 5q
# int64 ask_price[5];   -> 5q
# int64 ask_volume[5];  -> 5q
# 总计有效字节: 16 + 8*6 + 8*5*4 = 224 字节
# C++ padding 补齐到 256 字节
STRUCT_FMT = "<16sqqqqqq5q5q5q5q"
STRUCT_LEN = struct.calcsize(STRUCT_FMT)

class BaseStrategy:
    def on_init(self): pass
    def on_tick(self, tick): pass
    def on_exit(self): pass

class DemoHighFreqStrategy(BaseStrategy):
    """
    示例：高频盘口策略
    """
    def __init__(self, logger, collector):
        self.logger = logger
        self.collector = collector
        self.pos = 0 # 模拟持仓

    def on_tick(self, tick):
        # 1. 简单的盘口压力因子计算
        # (Bid1_Vol - Ask1_Vol) / (Bid1_Vol + Ask1_Vol)
        bid1_vol = tick['bid_volume'][0]
        ask1_vol = tick['ask_volume'][0]
        
        if bid1_vol + ask1_vol == 0: return

        imbalance = (bid1_vol - ask1_vol) / (bid1_vol + ask1_vol)
        
        # 2. 交易信号
        action = "HOLD"
        if imbalance > 0.6 and self.pos == 0:
            action = "BUY"
            self.pos = 1
            print(f"[{tick['symbol']}] 🚀 BUY SIGNAL @ {tick['last_price']} (Imbalance: {imbalance:.2f})")
        elif imbalance < -0.6 and self.pos > 0:
            action = "SELL"
            self.pos = 0
            print(f"[{tick['symbol']}] 📉 SELL SIGNAL @ {tick['last_price']}")

        # 3. 记录特征 (用于训练)
        if action != "HOLD":
            self.collector.snapshot(
                symbol=tick['symbol'],
                timestamp=tick['timestamp'],
                factors={"imbalance": imbalance, "spread": tick['ask_price'][0] - tick['bid_price'][0]},
                action=action
            )
        
        # 4. 记录日志 (用于性能分析)
        return {"imbalance": imbalance, "action": action}

class StrategyEngine:
    def __init__(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.settimeout(1.0) # 非阻塞 Loop
        
        # 初始化组件
        self.logger = StrategyLogger(strategy_name="HFT_Demo_01")
        self.collector = FeatureCollector()
        
        # 加载策略
        self.strategy = DemoHighFreqStrategy(self.logger, self.collector)
        
        print(f"✅ 策略引擎已启动，监听 UDP 端口 {UDP_PORT}...")
        print(f"✅ 期望数据包格式长度: {STRUCT_LEN} 字节")

    def run(self):
        self.strategy.on_init()
        
        while self.running:
            try:
                data, _ = self.sock.recvfrom(BUFFER_SIZE)
                
                # 性能计时开始
                t0 = time.perf_counter_ns()
                
                if len(data) < STRUCT_LEN:
                    continue # 忽略不完整包
                
                # 1. 极速解包
                unpacked = struct.unpack(STRUCT_FMT, data[:STRUCT_LEN])
                
                # 2. 构建 Tick 字典 (比 Class 更快)
                symbol_bytes = unpacked[0]
                symbol = symbol_bytes.decode('utf-8').rstrip('\x00')
                
                tick = {
                    'symbol': symbol,
                    'timestamp': unpacked[1],
                    'local_time': unpacked[2],
                    'last_price': unpacked[3] / 10000.0,
                    'volume': unpacked[4],
                    'turnover': unpacked[5],
                    'open_interest': unpacked[6],
                    'bid_price': [x / 10000.0 for x in unpacked[7:12]],
                    'bid_volume': list(unpacked[12:17]),
                    'ask_price': [x / 10000.0 for x in unpacked[17:22]],
                    'ask_volume': list(unpacked[22:27])
                }
                
                # 3. 策略回调
                decision = self.strategy.on_tick(tick)
                
                # 4. 性能统计
                t1 = time.perf_counter_ns()
                cost_ns = t1 - t0
                
                # 仅在有决策或低频采样时记录日志，避免日志 I/O 拖慢系统
                if decision:
                    self.logger.log_execution("on_tick", tick['timestamp'], cost_ns, decision)
                
            except socket.timeout:
                pass # 心跳或空转
            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                print(f"[Engine Error] {e}")

    def stop(self):
        self.running = False
        self.strategy.on_exit()
        self.logger.close()
        self.collector.flush()
        print("策略引擎安全退出。")

if __name__ == "__main__":
    engine = StrategyEngine()
    engine.run()