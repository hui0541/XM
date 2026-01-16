import os
import json
import shutil
import time
import logging
from typing import Dict, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelRegistry:
    """
    模型注册表与版本管理器
    职责：注册新模型、晋升生产版本、一键回滚
    """
    def __init__(self, metadata_path="./model_registry.json", base_dir="./models"):
        self.metadata_path = metadata_path
        self.base_dir = base_dir
        
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {"production": None, "history": []}
        return {"production": None, "history": []}

    def _save_registry(self):
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=4, ensure_ascii=False)

    def register_version(self, algo_name: str, file_path: str, metrics: Dict) -> str:
        """
        注册一个新训练好的模型版本
        """
        version_id = f"v_{int(time.time())}"
        target_path = os.path.join(self.base_dir, f"{algo_name}_{version_id}.model")
        
        # 归档模型文件
        shutil.copy2(file_path, target_path)
        
        entry = {
            "version": version_id,
            "algo": algo_name,
            "path": target_path,
            "metrics": metrics,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "candidate" # 候选状态
        }
        
        self.registry["history"].append(entry)
        self._save_registry()
        logging.info(f"✅ 模型版本已注册: {version_id} (Score: {metrics.get('score', 0):.4f})")
        return version_id

    def promote_to_production(self, version_id: str) -> bool:
        """
        将指定版本晋升为生产版 (Production)
        自动备份当前生产版为 Previous，以便回滚
        """
        candidate = self._find_version(version_id)
        if not candidate:
            logging.error(f"❌ 未找到版本: {version_id}")
            return False

        # 1. 记录旧版本 (用于回滚)
        current_prod = self.registry.get("production")
        if current_prod and current_prod['version'] != version_id:
            self.registry["previous"] = current_prod
            logging.info(f"🔄 当前生产版 {current_prod['version']} 已备份为 Previous")

        # 2. 更新生产版
        candidate['status'] = "production"
        candidate['promoted_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.registry["production"] = candidate
        
        self._save_registry()
        logging.info(f"🚀 版本 {version_id} 已晋升为 Production")
        return True

    def rollback(self) -> bool:
        """
        🚨 紧急回滚：切换回上一个生产版本
        """
        prev = self.registry.get("previous")
        if not prev:
            logging.warning("⚠️ 无法回滚：没有 Previous 版本记录")
            return False
            
        current = self.registry.get("production")
        logging.warning(f"🔙 正在从 {current['version']} 回滚到 {prev['version']} ...")
        
        # 交换指针
        self.registry["production"] = prev
        # 当前错误的版本变为“废弃”或保留在历史中，这里简单清除 previous 指针防止循环回滚
        self.registry["previous"] = None 
        
        self._save_registry()
        logging.info("✅ 回滚成功！")
        return True

    def get_production_model(self) -> Optional[str]:
        """ 获取当前生产模型路径 """
        prod = self.registry.get("production")
        if prod and os.path.exists(prod['path']):
            return prod['path']
        return None

    def _find_version(self, version_id):
        for v in self.registry["history"]:
            if v['version'] == version_id:
                return v
        return None

# 测试代码
if __name__ == "__main__":
    reg = ModelRegistry()
    # 模拟注册
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        reg.register_version("XGB_Demo", tmp.name, {"score": 0.85})