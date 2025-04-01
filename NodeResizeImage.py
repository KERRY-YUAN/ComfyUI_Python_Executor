"""
Resizes the image based on the target short side (`num`), maintaining aspect ratio, with final width and height both rounded up (ceil) to the nearest multiple of 16.
根据目标短边 (`num`) 调整图像大小，保持宽高比，最终宽高均向上取整为 16 的倍数。
"""

import torch
import math
from PIL import Image
import numpy as np

class NodeResizeImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "shortside": ("INT", {"default": 1024, "min": 560, "max": 9600, "step": 16}),
            }
        }
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image_resize", "width", "height")
    FUNCTION = "resize_image"
    CATEGORY = "Image/Transform"

    def _tensor_to_pil(self, img_tensor):
        # Convert ComfyUI IMAGE tensor to PIL Image / 将 ComfyUI IMAGE 张量转换为 PIL 图像。
        img_np = img_tensor[0].cpu().numpy() * 255.0
        img_np = np.clip(img_np, 0, 255).astype(np.uint8)[:, :, :3]
        return Image.fromarray(img_np, 'RGB')

    def _pil_to_tensor(self, img_pil):
        # Convert PIL Image to ComfyUI IMAGE tensor / 将 PIL 图像转换为 ComfyUI IMAGE 张量。
        img_np = np.array(img_pil).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    def resize_image(self, image, shortside):
        img_pil = self._tensor_to_pil(image)
        original_w, original_h = img_pil.size
        # Determine target short side (ceil to multiple of 16, min 16) / 计算目标短边（确保16的倍数）
        num_clamped = max(560, min(shortside, 9600))
        target_short = math.ceil(num_clamped / 16) * 16
        # Calculate scale and target long side / 计算最终尺寸
        if original_w <= original_h:
            scale = target_short / original_w
            final_h = math.ceil(original_h * scale / 16) * 16
            final_w = target_short
        else:
            scale = target_short / original_h
            final_w = math.ceil(original_w * scale / 16) * 16
            final_h = target_short
        # Resize the image using LANCZOS filter / 使用 LANCZOS 滤镜调整图像大小
        if (original_w, original_h) != (final_w, final_h):
            img_pil = img_pil.resize((final_w, final_h), Image.Resampling.LANCZOS)
        return (self._pil_to_tensor(img_pil), final_w, final_h)