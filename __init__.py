from .node_python_executor import NodePythonExecutor
from .node_resize_image import NodeResizeImage
from .node_auto_sampler import NodeAutoSampler

# --- Node Registration / 节点注册 ---
NODE_CLASS_MAPPINGS = {
    # Mapping key and class name / 映射键和类名
    "NodePython": NodePythonExecutor,
    "NodeResizeImage": NodeResizeImage,
    "NodeAutoSampler": NodeAutoSampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
     # Display name / 显示名称
    "NodePython": "NodePython",
    "NodeResizeImage": "NodeResizeImage",
    "NodeAutoSampler": "NodeAutoSampler"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS",]