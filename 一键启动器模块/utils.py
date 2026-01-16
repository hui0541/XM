import os
import sys
import time
import socket
import yaml
import psutil
from typing import Dict, Any

class SystemUtils:
    """
    系统工具集 - 专注于高性能和系统级操作
    """

    @staticmethod
    def load_config(filepath: str) -> Dict[str, Any]:
        """加载YAML配置，带容错处理"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"配置文件未找到: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"配置文件解析失败: {e}")

    @staticmethod
    def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
        """
        极速端口探测 (TCP Connect)
        :param timeout: 毫秒级超时，避免阻塞主线程太久
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except:
            return False
        finally:
            sock.close()

    @staticmethod
    def kill_process_tree(pid: int):
        """
        深度清理：递归结束进程及其所有子进程
        """
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass
            parent.terminate()
            # 给 3秒 优雅退出，否则强杀
            _, alive = psutil.wait_procs(children + [parent], timeout=3)
            for p in alive:
                p.kill()
        except psutil.NoSuchProcess:
            pass

    @staticmethod
    def get_timestamp_ms() -> int:
        """获取毫秒级时间戳，用于性能埋点"""
        return int(time.time() * 1000)