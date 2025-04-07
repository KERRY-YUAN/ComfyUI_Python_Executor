from .NodePythonExecutor import NodePythonExecutor

# --- Node Registration / 节点注册 ---
NODE_CLASS_MAPPINGS = {
    # Mapping key and class name / 映射键和类名
    "NodePython": NodePythonExecutor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
     # Display name / 显示名称
    "NodePython": "NodePython",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS",]