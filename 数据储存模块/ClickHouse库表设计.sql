-- 修改行情表或创建环境因子快照表
CREATE TABLE IF NOT EXISTS market_environment_history (
    ts DateTime64(3),
    sentiment_score Float32,   -- 赚钱效应得分
    index_name String,         -- 关联指数 (000300)
    index_momentum Float32,    -- 指数动能
    limit_up_count UInt32,     -- 全市场涨停家数
    limit_down_count UInt32    -- 全市场跌停家数
) ENGINE = MergeTree() ORDER BY ts;