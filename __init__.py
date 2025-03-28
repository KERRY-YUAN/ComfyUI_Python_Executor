from .node_python_executor import NodePythonExecutor
from .node_resize_image import NodeResizeImage

# --- Node Registration / 节点注册 ---
NODE_CLASS_MAPPINGS = {
    # Mapping key and class name / 映射键和类名
    "NodePython": NodePythonExecutor,
    "NodeResizeImage": NodeResizeImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
     # Display name / 显示名称
    "NodePython": "NodePython",
    "NodeResizeImage": "NodeResizeImage"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS",]