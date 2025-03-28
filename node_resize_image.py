# -*- coding: utf-8 -*-

import torch
import numpy as np
from PIL import Image
import math

class NodeResizeImage:
    # A node to resize an image based on a target short side ('num'), ensuring final dimensions are multiples of 16 (using ceil). / 根据目标短边 ('num') 调整图像大小的节点，确保最终尺寸是16的倍数（向上取整）。
    @classmethod
    def INPUT_TYPES(cls):
        # Define node inputs / 定义节点输入
        return {
            "required": {
                "image": ("IMAGE",), # Input image tensor / 输入图像张量
                # 'num' defines the base for the target short side, Default 1024, min 560, max 9600, step 16 / 'num' 定义目标短边的基准值, 默认 1024, 最小 560, 最大 9600, 步长 16
                "num": ("INT", {
                    "default": 1024,
                    "min": 560,
                    "max": 9600,
                    "step": 16
                }),
            }
        }

    # Define node outputs / 定义节点输出
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image_resize", "width", "height")
    FUNCTION = "resize_image"
    CATEGORY = "Image/Transform"

    def _tensor_to_pil(self, img_tensor: torch.Tensor) -> Image.Image:
        # Convert ComfyUI IMAGE tensor to PIL Image / 将 ComfyUI IMAGE 张量转换为 PIL 图像。
        if img_tensor is None or img_tensor.dim() != 4 or img_tensor.shape[0] == 0:
            raise ValueError("Invalid image tensor provided for PIL conversion.")
        img_np = img_tensor[0].cpu().numpy() * 255.0
        img_np = np.clip(img_np, 0, 255).astype(np.uint8)
        if img_np.shape[2] == 1:
             return Image.fromarray(img_np[:, :, 0], 'L').convert('RGB')
        elif img_np.shape[2] == 3:
             return Image.fromarray(img_np, 'RGB')
        else:
            if img_np.shape[2] == 4:
                print("[Resize Image Node] Warning: Input tensor has 4 channels (RGBA?), converting to RGB.")
                return Image.fromarray(img_np[:, :, :3], 'RGB')
            else:
                print(f"[Resize Image Node] Warning: Input tensor has {img_np.shape[2]} channels, attempting conversion to RGB.")
                try:
                    return Image.fromarray(img_np).convert('RGB')
                except Exception as e:
                    raise ValueError(f"Could not convert tensor with shape {img_np.shape} to RGB PIL Image: {e}")


    def _pil_to_tensor(self, img_pil: Image.Image) -> torch.Tensor:
        # Convert PIL Image to ComfyUI IMAGE tensor / 将 PIL 图像转换为 ComfyUI IMAGE 张量。
        if img_pil.mode != 'RGB':
            img_pil = img_pil.convert('RGB')
        img_np = np.array(img_pil).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np).unsqueeze(0)
        return img_tensor

    def resize_image(self, image: torch.Tensor, num: int):
        # Resizes the image based on 'num' as the target short side, ensuring dimensions are multiples of 16 using ceil. / 根据 'num' 作为目标短边调整图像大小，确保尺寸是16的倍数（向上取整）。
        try:
            img_pil = self._tensor_to_pil(image)
        except ValueError as e:
            print(f"[Resize Image Node] Error converting input tensor: {e}")
            h, w = image.shape[1:3] if image is not None and image.dim()==4 else (0,0)
            return (image, w, h)

        original_w, original_h = img_pil.size

        num = max(560, min(9600, num))

        # 1. Determine target short side (ceil to multiple of 16, min 16) / 1. 确定目标短边长度 (向上取整到16的倍数, 且至少为16)
        target_short_side_base = max(16, num)
        target_short_side = math.ceil(target_short_side_base / 16.0) * 16
        target_short_side = max(16, target_short_side)

        # 2. Calculate scale and target long side (ceil to multiple of 16, min 16) / 2. 计算缩放比例和目标长边长度 (向上取整到16的倍数, 且至少为16)
        if original_w == 0 or original_h == 0:
            print(f"[Resize Image Node] Error: Original image dimensions are zero ({original_w}x{original_h}). Cannot resize.")
            h, w = image.shape[1:3] if image is not None and image.dim()==4 else (0,0)
            return (image, w, h)

        if original_w < original_h:
            if original_w == 0: scale = 0
            else: scale = target_short_side / original_w
            target_long_side_initial = original_h * scale
            final_w = target_short_side
            final_h = max(16, math.ceil(target_long_side_initial / 16.0) * 16)
        elif original_h < original_w:
             if original_h == 0: scale = 0
             else: scale = target_short_side / original_h
             target_long_side_initial = original_w * scale
             final_h = target_short_side
             final_w = max(16, math.ceil(target_long_side_initial / 16.0) * 16)
        else:
             final_w = target_short_side
             final_h = target_short_side


        print(f"[Resize Image Node] Original: {original_w}x{original_h}, Input 'num': {num}, Target Short Base: {target_short_side_base}, Target Short Side (x16 ceil): {target_short_side}, Final Target: {final_w}x{final_h}")

        # 3. Resize the image using LANCZOS filter / 3. 使用 LANCZOS 滤镜调整图像大小
        final_w, final_h = int(final_w), int(final_h)

        if final_w <= 0 or final_h <= 0:
             print(f"[Resize Image Node] Error: Calculated final dimensions are invalid ({final_w}x{final_h}). Returning original.")
             return (image, original_w, original_h)

        try:
            if (original_w, original_h) == (final_w, final_h):
                resized_img_pil = img_pil
                print(f"[Resize Image Node] Input dimensions already match target. Skipping resize.")
            else:
                resized_img_pil = img_pil.resize((final_w, final_h), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"[Resize Image Node] Error during PIL resize: {e}")
            return (image, original_w, original_h)

        # 4. Convert resized PIL image back to tensor / 4. 将调整大小后的 PIL 图像转换回张量
        try:
            resized_image_tensor = self._pil_to_tensor(resized_img_pil)
        except Exception as e:
             print(f"[Resize Image Node] Error converting resized PIL image back to tensor: {e}")
             return(image, original_w, original_h)


        # Return resized image tensor and final dimensions / 返回调整大小后的图像张量和最终尺寸
        return (resized_image_tensor, final_w, final_h)