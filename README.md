# ComfyUI_Python_Executor
This node includes a node for custom Python input within ComfyUI.
本节点包含一个在ComfyUI 中自定义输入python的节点。


## Node List

### NodePythonExecutor (`NodePython`)
*   Category: DevTools
*   Node Type: Python Code Execution


## Node Descriptions

### NodePythonExecutor (`NodePython`)

*   **Description**: Executes Python code within the ComfyUI workflow. Inputs can be accessed via `anyA`-`anyF`, and outputs are defined by assigning values to variables like `num1`-`any3`. Captures `print` output into `text2`.
*   **Category**: `DevTools`
*   **Inputs**:
    *   `code` (STRING, multiline): Python code to be executed (Inputs `anyA` to `anyF` are accessible internally).
    *   (Optional) `anyA` - `anyF` (ANY): Data passed to the script.
*   **Outputs**:
    *   Defined by assignment within the code:
        *   `num1` (INT), `num2` (FLOAT)
        *   `text1` (STRING), `text2` (STRING, includes `print` output)
        *   `any1` (ANY), `any2` (ANY), `any3` (ANY)
*   **Usage Example**:
    *   **Goal**: Input number 5 (`anyA`) and string "hello" (`anyB`), output the number plus 10, the uppercase string, and print a message.
    *   **Code (`code` input)**:
        ```python
        print(f"Received anyA: {anyA}, anyB: {anyB}")
        num1 = anyA + 10 if anyA is not None else -1
        text1 = anyB.upper() if isinstance(anyB, str) else "Input B is not a string"
        any1 = f"Processed {anyA} and {anyB}"
        ```
    *   **Expected Output**:
        *   `num1`: `15`
        *   `text1`: `"HELLO"`
        *   `text2`: Contains `print` output like "Received anyA: 5, anyB: hello".
        *   `any1`: `"Processed 5 and hello"`
   
![image](https://github.com/KERRY-YUAN/ComfyUI_Python_Executor/blob/main/Examples/Node_python_executor_ResizeImage_16ceil.png)
---

## Installation Steps

### 1. Clone this repository to ComfyUI's custom_nodes directory:
*   cd /path/to/comfyui/custom_nodes  # Custom node location
*   git clone https://github.com/KERRY-YUAN/ComfyUI_Python_Executor.git
### 2. Restart ComfyUI.


## 节点列表

### NodePythonExecutor (`NodePython`)

## 节点说明

### NodePythonExecutor (`NodePython`)

*   **描述**: 在 ComfyUI 工作流中执行 Python 代码。可通过 `anyA`-`anyF` 访问输入，通过赋值给 `num1`-`any3` 等变量定义输出。捕获 `print` 输出到 `text2`。
*   **分类**: `DevTools`
*   **输入**:
    *   `code` (STRING, 多行): 待执行 Python 代码 (内部可访问 `anyA` 至 `anyF` 输入)。
    *   (可选) `anyA` - `anyF` (ANY): 传递给脚本的数据。
*   **输出**:
    *   通过在代码中赋值定义：
        *   `num1` (INT), `num2` (FLOAT)
        *   `text1` (STRING), `text2` (STRING, 包含 `print` 输出)
        *   `any1` (ANY), `any2` (ANY), `any3` (ANY)
*   **使用范例**:
    *   **目标**: 输入数字 5 (`anyA`) 和字符串 "hello" (`anyB`)，输出加 10 后的数字、大写字符串，并打印信息。
    *   **代码 (`code` 输入)**:
        ```python
        print(f"接收到 anyA: {anyA}, anyB: {anyB}")
        num1 = anyA + 10 if anyA is not None else -1
        text1 = anyB.upper() if isinstance(anyB, str) else "输入 B 不是字符串"
        any1 = f"处理了 {anyA} 和 {anyB}"
        ```
    *   **预期输出**:
        *   `num1`: `15`
        *   `text1`: `"HELLO"`
        *   `text2`: 包含 "接收到 anyA: 5, anyB: hello" 等 `print` 输出。
        *   `any1`: `"处理了 5 和 hello"`
---

## 安装步骤


### 1. 克隆本仓库到 ComfyUI 的 `custom_nodes` 目录：
*   cd /path/to/comfyui/custom_nodes（自定义节点位置）
*   git clone https://github.com/KERRY-YUAN/ComfyUI_Python_Executor.git
### 2. 重启 ComfyUI。
