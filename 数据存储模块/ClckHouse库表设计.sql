-- 创建数据库
CREATE DATABASE IF NOT EXISTS speed_trader;

USE speed_trader;

-- ==========================================
-- 行情快照表 (MergeTree 引擎)
-- 优化点：
-- 1. ORDER BY (symbol, timestamp) 确保单标的时间序列查询最快
-- 2. DateTime64(3) 存储毫秒级精度
-- 3. 数组结构存储五档行情，减少列数，提升压缩率
-- ==========================================
CREATE TABLE IF NOT EXISTS market_ticks (
    symbol String COMMENT '合约代码',
    timestamp DateTime64(3) COMMENT '交易所时间戳',
    local_time DateTime64(3) COMMENT '本地接收时间',
    
    last_price Float64 COMMENT '最新价',
    volume Int64 COMMENT '成交量',
    turnover Float64 COMMENT '成交额',
    open_interest Int64 COMMENT '持仓量',
    
    -- 五档行情使用 Array 存储 [Ask1, Ask2...]
    bid_price Array(Float64),
    bid_volume Array(Int64),
    ask_price Array(Float64),
    ask_volume Array(Int64),
    
    date Date DEFAULT toDate(timestamp) COMMENT '分区日期'
) ENGINE = MergeTree()
PARTITION BY date
ORDER BY (symbol, timestamp)
SETTINGS index_granularity = 8192;