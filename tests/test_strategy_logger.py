import importlib.util
import json
import pathlib
import tempfile
import unittest


def load_strategy_logger_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "策略引擎模块" / "策略运行日志.py"
    spec = importlib.util.spec_from_file_location("strategy_logger", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StrategyLoggerTests(unittest.TestCase):
    def test_close_flushes_buffered_logs(self):
        strategy_logger = load_strategy_logger_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = strategy_logger.StrategyLogger(
                log_dir=temp_dir,
                strategy_name="TestStrategy",
            )
            logger.log_execution("on_tick", 123, 1000, {"action": "BUY"})
            logger.close()

            log_path = pathlib.Path(temp_dir) / "strategy_TestStrategy.jsonl"
            self.assertTrue(log_path.exists())

            lines = log_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record["algo"], "TestStrategy")
