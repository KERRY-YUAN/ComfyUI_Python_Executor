"""
Author: "KERRY-YUAN",
Title: "NodePython",
Git-clone: "https://github.com/KERRY-YUAN/ComfyUI_Simple_Executor",
This node executes Python code directly within the ComfyUI workflow.
此节点直接在 ComfyUI 工作流中执行 Python 代码。
"""

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