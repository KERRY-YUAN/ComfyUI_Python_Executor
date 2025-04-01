"""
This node executes Python code directly within the ComfyUI workflow.
此节点直接在 ComfyUI 工作流中执行 Python 代码。
"""

import tempfile
import os
import runpy
import sys
import io
import traceback
from typing import Dict, Any, Optional, List

# --- ComfyUI AnyType definition / ComfyUI AnyType 定义 ---
class AnyType(str):
    # Special type for ComfyUI wildcard connections / ComfyUI 通配符连接的特殊类型
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True # Assume compatible / 假设兼容

any = AnyType("*")
# --- End ComfyUI AnyType definition / 结束 ComfyUI AnyType 定义 ---

# Renamed class / 重命名类
class NodePythonExecutor:

    @classmethod
    def INPUT_TYPES(cls):
        # Define node inputs / 定义节点输入
        return {
            "required": {
                "code": ("STRING", {"multiline": True, "default": "# Enter Python code...\n# Inputs: anyA-anyF\n# Outputs: num1,num2,text1,text2,any1-any3"}),
            },
            "optional": {
                "anyA": (any, {}), "anyB": (any, {}), "anyC": (any, {}),
                "anyD": (any, {}), "anyE": (any, {}), "anyF": (any, {}),
            }
        }

    # Define node outputs / 定义节点输出
    RETURN_TYPES = (any, any, any, any, any, any, any)
    RETURN_NAMES = ("num1", "num2", "text1", "text2", "any1", "any2", "any3")
    FUNCTION = "execute_code"
    CATEGORY = "DevTools"

    # Execute_code signature / execute_code 签名
    def execute_code(self, code: str, anyA: Optional[Any] = None, anyB: Optional[Any] = None, anyC: Optional[Any] = None, anyD: Optional[Any] = None, anyE: Optional[Any] = None, anyF: Optional[Any] = None) -> tuple:
        """Executes user Python code directly via runpy.run_path / 通过 runpy.run_path 直接执行用户 Python 代码"""
        # Default return values for errors / 错误的默认返回值
        default_outputs = (0, 0.0, "", "", None, None, None)

        try:
            # Prepare execution environment / 准备执行环境
            globals_dict = {'anyA': anyA, 'anyB': anyB, 'anyC': anyC, 'anyD': anyD, 'anyE': anyE, 'anyF': anyF}
            tmp_filename = None
            printed_output = ""
            old_stdout = sys.stdout
            redirected_output = io.StringIO()

            try:
                # Create and execute code in temporary file / 在临时文件中创建并执行代码
                with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding='utf-8') as tmp_file:
                    tmp_file.write(code)
                    tmp_filename = tmp_file.name

                sys.stdout = redirected_output # Redirect stdout / 重定向 stdout
                result_globals = runpy.run_path(tmp_filename, init_globals=globals_dict) # Execute code / 执行代码
                sys.stdout = old_stdout # Restore stdout / 恢复标准输出
                printed_output = redirected_output.getvalue().strip()

                # Retrieve outputs / 检索输出
                num1_out = result_globals.get('num1', default_outputs[0])
                num2_out = result_globals.get('num2', default_outputs[1])
                text1_out = result_globals.get('text1', default_outputs[2])
                text2_out = result_globals.get('text2', default_outputs[3])
                any1_out = result_globals.get('any1', default_outputs[4])
                any2_out = result_globals.get('any2', default_outputs[5])
                any3_out = result_globals.get('any3', default_outputs[6])

                # Append printed output / 附加打印输出
                if printed_output:
                    text2_out = (text2_out + "\n" if text2_out else "") + "--- Printed Output ---\n" + printed_output

                # Return successful results / 返回成功执行的结果
                return num1_out, num2_out, text1_out, text2_out, any1_out, any2_out, any3_out

            # Handle user code errors / 处理用户代码错误
            except SyntaxError as e:
                 sys.stdout = old_stdout
                 print(f"[NodePython] Syntax Error: {e}")
                 return (default_outputs[0], default_outputs[1], f"Syntax Error: {e}", printed_output, *default_outputs[4:])
            except ImportError as e:
                 sys.stdout = old_stdout
                 print(f"[NodePython] Import Error: {e}")
                 return (default_outputs[0], default_outputs[1], f"Import Error: {e}", printed_output, *default_outputs[4:])
            except Exception as e:
                # Catch other execution errors / 捕获其他执行错误
                sys.stdout = old_stdout
                tb_str = traceback.format_exc()
                print(f"[NodePython] Execution Error: {e}\n{tb_str[:1000]}...")
                return (default_outputs[0], default_outputs[1], f"Execution Error: {e}", tb_str, *default_outputs[4:])
            finally:
                 # Final cleanup / 最后清理
                 if sys.stdout != old_stdout: sys.stdout = old_stdout
                 if tmp_filename and os.path.exists(tmp_filename):
                    try: os.remove(tmp_filename)
                    except Exception as e_clean: print(f"[NodePython] Error cleaning temp file: {e_clean}")

        # Catch unexpected node errors / 捕获意外的节点错误
        except Exception as e:
            tb_str = traceback.format_exc()
            print(f"[NodePython] Unexpected Node Error: {e}\n{tb_str[:1000]}...")
            return (default_outputs[0], default_outputs[1], f"Unexpected Node Error: {e}", tb_str, *default_outputs[4:])