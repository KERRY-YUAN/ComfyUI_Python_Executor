# ComfyUI_Python_Executor
This node includes a node for custom Python input within ComfyUI, along with several other convenient processing nodes. Subject to occasional updates.
本节点包含一个在ComfyUI 中自定义输入python的节点，和一些便捷处理节点。不定时更新中


## Node List

### 1. NodePythonExecutor (`NodePython`)
*   Category: DevTools
*   Node Type: Python Code Execution
### 2. NodeResizeImage (`NodeResizeImage`)
*   Category: Image/Transform
*   Node Type: Image Resizing

## Node Descriptions

### 1. NodePythonExecutor (`NodePython`)

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
---
### 2. NodeResizeImage (`NodeResizeImage`)

*   **Description**: Resizes the image based on the target short side (`num`), maintaining aspect ratio, with final width and height both rounded up (ceil) to the nearest multiple of 16.
*   **Category**: `Image/Transform`
*   **Inputs**:
    *   `image` (IMAGE): Image to be resized.
    *   `num` (INT): Target short side base value (default 1024, range 560-9600).
*   **Outputs**:
    *   `image_resize` (IMAGE): The resized image.
    *   `width` (INT): Final width (multiple of 16).
    *   `height` (INT): Final height (multiple of 16).
*   **Usage Example**:
    *   **Goal**: Resize an `800x600` image, setting the target short side to `768`.
    *   **Setup**: Input `800x600` image, `num` set to `768`.
    *   **Process**:
        1. Short side 600, long side 800.
        2. Target short side rounded up to multiple of 16 -> `768`.
        3. Calculate target long side proportionally -> `800 * (768 / 600) = 1024`.
        4. Target long side rounded up to multiple of 16 -> `1024`.
        5. Final dimensions are `1024x768`.
    *   **Expected Output**:
        *   `image_resize`: Image with dimensions `1024x768`.
        *   `width`: `1024`
        *   `height`: `768`
---

## Installation Steps

### 1. Clone this repository to ComfyUI's custom_nodes directory:
*   cd /path/to/comfyui/custom_nodes  # Custom node location
*   git clone https://github.com/KERRY-YUAN/ComfyUI_Python_Executor.git
### 2. Restart ComfyUI.


## 节点列表

### 1. NodePythonExecutor (`NodePython`)
### 2. NodeResizeImage (`NodeResizeImage`)

## 节点说明

### 1. NodePythonExecutor (`NodePython`)

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
### 2. NodeResizeImage (`NodeResizeImage`)

*   **描述**: 根据目标短边 (`num`) 调整图像大小，保持宽高比，最终宽高均向上取整为 16 的倍数。
*   **分类**: `Image/Transform`
*   **输入**:
    *   `image` (IMAGE): 待调整图像。
    *   `num` (INT): 目标短边基准值 (默认 1024, 范围 560-9600)。
*   **输出**:
    *   `image_resize` (IMAGE): 调整后的图像。
    *   `width` (INT): 最终宽度 (16的倍数)。
    *   `height` (INT): 最终高度 (16的倍数)。
*   **使用范例**:
    *   **目标**: 将 `800x600` 图像的短边目标设为 `768` 进行调整。
    *   **设置**: 输入 `800x600` 图像, `num` 设为 `768`。
    *   **过程**:
        1. 短边 600, 长边 800。
        2. 目标短边向上取整到 16 倍数 -> `768`。
        3. 按比例计算目标长边 -> `800 * (768 / 600) = 1024`。
        4. 目标长边向上取整到 16 倍数 -> `1024`。
        5. 最终尺寸为 `1024x768`。
    *   **预期输出**:
        *   `image_resize`: `1024x768` 尺寸的图像。
        *   `width`: `1024`
        *   `height`: `768`
---

## 安装步骤


### 1. 克隆本仓库到 ComfyUI 的 `custom_nodes` 目录：
*   cd /path/to/comfyui/custom_nodes（自定义节点位置）
*   git clone https://github.com/KERRY-YUAN/ComfyUI_Python_Executor.git
### 2. 重启 ComfyUI。
