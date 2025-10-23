<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>admin</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<body>
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="../api/cpri_add" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加CPR信息</h2>

            <div class="form-group">
                <label>区域名称</label>
                <input type="text" name="name" class="form-control" value=""
                    placeholder="请输入区域名称" required>
            </div>

            <div class="form-group">
                <label>描述</label>
                <input type="text" name="description" class="form-control" value=""
                    placeholder="请输入描述" required>
            </div>

            <div class="form-group">
                <label>绑定CPRD设备(仅限在线CPRD设备，离线设备必须连接到服务器后才能绑定)</label>
                <select class="form-control" name="cprd_id" id="cprd_id" onchange="loadImage()">
                    % for availableCPRDevice in availableCPRDeviceData:
                    <option value="{{availableCPRDevice.id}}">{{availableCPRDevice.name}}(MID:{{availableCPRDevice.machine_id}})</option>
                    % end
                </select>
            </div>

            <!-- 图片显示框 -->
            <div class="form-group">
                <label>选择图片并标记坐标</label>
                <div id="image-container" style="width: 100%;  background-color: #f0f0f0; text-align: center; position: relative;">
                    <img id="image" src="../static/images/background.png" alt="图片" style="width: 100%;" />
                    <div id="coordinates" style="position: absolute; top: 0; left: 0;"></div>
                </div>
            </div>

            <div class="form-group">
                <label>X1</label>
                <input type="number" name="x1" id="x1" class="form-control" value=""
                    placeholder="请输入X1坐标" required readonly>
            </div>

            <div class="form-group">
                <label>Y1</label>
                <input type="number" name="y1" id="y1" class="form-control" value=""
                    placeholder="请输入Y1坐标" required readonly>
            </div>

            <div class="form-group">
                <label>X2</label>
                <input type="number" name="x2" id="x2" class="form-control" value=""
                    placeholder="请输入X2坐标" required readonly>
            </div>

            <div class="form-group">
                <label>Y2</label>
                <input type="number" name="y2" id="y2" class="form-control" value=""
                    placeholder="请输入Y2坐标" required readonly>
            </div>

            <!-- 不可修改字段：占用状态，车牌号，图片 -->
            <div class="form-group" hidden>
                <label>占用状态</label>
                <input type="text" class="form-control" value="空闲" disabled>
            </div>

            <div class="form-group" hidden>
                <label>车牌号</label>
                <input type="text" class="form-control" value="" disabled>
            </div>

            <div class="form-group" hidden>
                <label>图片</label>
                <textarea class="form-control" disabled></textarea>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%;">添 加</button>
        </form>
    </div>

    <script>
        let isFirstClick = true;
        let x1 = null, y1 = null, x2 = null, y2 = null;
        const coordinatesDiv = document.getElementById('coordinates');
        const x1Input = document.getElementById('x1');
        const y1Input = document.getElementById('y1');
        const x2Input = document.getElementById('x2');
        const y2Input = document.getElementById('y2');
        const imageContainer = document.getElementById('image-container');
        const image = document.getElementById('image');

        // 捕获图片点击坐标
        imageContainer.addEventListener('click', function (event) {
            const rect = image.getBoundingClientRect(); // 获取图片的显示区域
            const imageWidth = image.naturalWidth; // 图片的原始宽度
            const imageHeight = image.naturalHeight; // 图片的原始高度
            const offsetX = event.clientX - rect.left; // 点击位置相对于图片容器的位置
            const offsetY = event.clientY - rect.top; // 点击位置相对于图片容器的位置

            // 计算缩放比例
            const scaleX = imageWidth / rect.width; // 宽度的缩放比例
            const scaleY = imageHeight / rect.height; // 高度的缩放比例

            // 还原到原始尺寸
            const originalX = offsetX * scaleX;
            const originalY = offsetY * scaleY;

            if (isFirstClick) {
                x1 = originalX;
                y1 = originalY;
                x1Input.value = x1;
                y1Input.value = y1;
                isFirstClick = false;

                // 绘制标记
                coordinatesDiv.innerHTML = `<div style="position: absolute; left: ${offsetX - 5}px; top: ${offsetY - 5}px; width: 10px; height: 10px; background: red; border-radius: 50%;"></div>`;
            } else {
                x2 = originalX;
                y2 = originalY;
                x2Input.value = x2;
                y2Input.value = y2;

                // 绘制第二个标记
                coordinatesDiv.innerHTML += `<div style="position: absolute; left: ${offsetX - 5}px; top: ${offsetY - 5}px; width: 10px; height: 10px; background: blue; border-radius: 50%;"></div>`;
                isFirstClick = true;
            }
        });

        // 右键点击退出标记
        imageContainer.addEventListener('contextmenu', function (event) {
            event.preventDefault();
            coordinatesDiv.innerHTML = '';  // 清除所有标记
            isFirstClick = true;  // 重置状态
            x1Input.value = '';
            y1Input.value = '';
            x2Input.value = '';
            y2Input.value = '';
        });
    </script>
    <script>
        function loadImage() {
            const cprdId = document.getElementById('cprd_id').value;
            const imageElement = document.getElementById('image');

            // 请求获取图片的 Base64 数据
            fetch(`../api/cpri_get_cprd_image?id=${cprdId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.image_base64) {
                        // 设置图片的src为Base64格式
                        imageElement.src = "data:image/png;base64," + data.image_base64;
                    } else {
                        alert("图像未找到");
                    }
                })
                .catch(error => {
                    console.error('Error fetching image:', error);
                    alert('获取图片失败');
                });
        }
                // 页面加载时自动触发图片加载，使用默认选择的 cprd_id
        window.onload = function() {
            loadImage();  // 页面加载时自动加载图片
        };
    </script>
</body>

</html>
