import torch
import math
from comfy.samplers import KSampler

class NodeAutoSampler:
    @classmethod
    def INPUT_TYPES(s):
        # 获取 ComfyUI 中的采样器名称列表
        sampler_names = KSampler.SAMPLERS
        return {
            "required": {
                "ckpt_name": ("STRING", {"default": ""}),
                "mode": (["Auto", "Light", "Normal", "User"], {"default": "Auto"})
            },
            "optional": {
                "light_steps": ("INT", {"default": 5, "min": 1, "max": 1000}),
                "light_cfg": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 100.0}),
                "light_sampler": (sampler_names, {"default": "dpmpp_sde"}),
                "normal_steps": ("INT", {"default": 30, "min": 1, "max": 1000}),
                "normal_cfg": ("FLOAT", {"default": 5.0, "min": 0.1, "max": 100.0}),
                "normal_sampler": (sampler_names, {"default": "dpmpp_2m_sde"}),
                "user_steps": ("INT", {"default": 20, "min": 1, "max": 1000}),
                "user_cfg": ("FLOAT", {"default": 3.5, "min": 0.1, "max": 100.0}),
                "user_sampler": (sampler_names, {"default": "dpmpp_2m_sde"})
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("steps", "cfg", "sampler", "text")
    FUNCTION = "generate_dynamic_settings"
    CATEGORY = "custom"

    def generate_dynamic_settings(self, ckpt_name, mode,
                                  light_steps=5, light_cfg=2.0, light_sampler="dpmpp_sde",
                                  normal_steps=30, normal_cfg=5.0, normal_sampler="dpmpp_2m_sde",
                                  user_steps=20, user_cfg=3.5, user_sampler="dpmpp_2m_sde"):
        input_str = str(ckpt_name).lower()
        mode_map = {
            "Auto": "0",
            "Light": "1",
            "Normal": "2",
            "User": "3"
        }
        input_int_str = mode_map[mode]

        mode = "2"  # Default
        if input_int_str in ["1", "2", "3"]:
            mode = input_int_str
        elif input_int_str == "0":
            if "light" in input_str or "turbo" in input_str:
                mode = "1"
            elif "userconfig" in input_str:
                mode = "3"

        if mode == "1":
            processed_string = f"{light_steps};{light_cfg};{light_sampler}"
        elif mode == "2":
            processed_string = f"{normal_steps};{normal_cfg};{normal_sampler}"
        else:  # mode == "3" or fallback
            processed_string = f"{user_steps};{user_cfg};{user_sampler}"

        parts = processed_string.split(';')
        steps_out = int(parts[0])
        cfg_out = float(parts[1])
        sampler_out = parts[2]

        return steps_out, cfg_out, sampler_out, processed_string
    