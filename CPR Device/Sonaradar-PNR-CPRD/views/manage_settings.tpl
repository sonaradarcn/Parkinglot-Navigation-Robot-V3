<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>settings</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<body>
    <div class="container mt-5" style="align-items: center; justify-content: center; display: flex;">
        <div style="width: 700px; margin-top: 20px; margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">CPRD设备参数设置</h2>
            <form action="" method="get">
                <h3 class="text-center mb-4" style="padding-top: 10px;">设备信息</h3>
                <div class="form-group">
                    <label>设备IP</label>
                    <input type="text" class="form-control" value="{{data_localIP}}" placeholder="" readonly>
                </div>
                <div class="form-group">
                    <label>设备机器码</label>
                    <input type="text" class="form-control" value="{{data_machineCode}}" placeholder="" readonly>
                    <label style="padding-top: 4px;">请在总管理面板绑定CPRD设备，绑定设备时请正确提供15位机器码。</label>
                </div>
            </form>
            <form action="../api/set_server_ip" method="get">
                <h3 class="text-center mb-4" style="padding-top: 10px;">服务器连接设置</h3>
                <div class="form-group">
                    <label>服务器IP</label>
                    <input type="text" name="server_ip" class="form-control" value="{{data_serverIP}}" placeholder="" >
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">修改服务器连接设置(修改后断开连接立即重联)</button>
            </form>
            <form action="../api/set_camera_index" method="get">
                <h3 class="text-center mb-4" style="padding-top: 10px;">摄像头设置</h3>
                <div class="form-group">
                    <label>摄像头选择</label>
                    <select class="form-control" name="camera_index" id="camera-select">
                        % for info in data_cameraList:
                        % if info['index'] == data_cameraIndex: 
                        <option value="{{info['index']}}" selected>索引:{{info['index']}}({{info['width']}}x{{info['height']}}@{{info['fps']}}fps)</option>
                        % else:
                        <option value="{{info['index']}}">索引:{{info['index']}}({{info['width']}}x{{info['height']}}@{{info['fps']}}fps)</option>
                        % end
                        % end
                    </select>
                    <div style="padding-top: 10px;">
                        <label>摄像头画面预览</label>
                        <div id="image-container" class="form-group">
                            <img id="image" style="width: 100%;border-radius: 5px;" src="">
                        </div>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">修改摄像头</button>
            </form>
            <form action="../api/set_recognization_enable" method="get">
                <h3 class="text-center mb-4" style="padding-top: 10px;">识别功能设置</h3>
                <div class="form-group">
                    <label>车牌识别状态</label>
                    <select class="form-control" name="cp_mode">
                        % if data_recognization_enable==True:
                        <option value="1" selected>正常识别</option>
                        <option value="0">暂停识别</option>
                        % else:
                        <option value="1">正常识别</option>
                        <option value="0" selected>暂停识别</option>
                        % end
                    </select>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">更改识别状态</button>
            </form>
            <form action="../api/set_user" method="get">
                <h3 class="text-center mb-4" style="padding-top: 10px;">登录设置</h3>
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" name="username" class="form-control" value="{{data_username}}" placeholder="请输入用户名" readonly>
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" name="password" class="form-control" value="" placeholder="请输入密码" >
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">修改登录信息</button>
            </form>

        </div>
    </div>
</body>

<script>
    // 获取当前选择的摄像头索引并刷新图像
    function refreshCameraImage(cameraIndex) {
        // 发起 AJAX 请求
        fetch('../api/get_camera_image?camera_index=' + cameraIndex)
            .then(response => response.json())
            .then(data => {
                // 更新图片的 src
                document.getElementById("image").src = "data:image/jpeg;base64," + data.image_base64;
            })
            .catch(error => console.error('Error:', error));
    }

    // 在页面加载时刷新图像（默认选择的摄像头）
    document.addEventListener("DOMContentLoaded", function() {
        var selectedCameraIndex = document.getElementById("camera-select").value;
        refreshCameraImage(selectedCameraIndex); // 刷新当前选中的摄像头图像
    });

    // 监听摄像头选择变化
    document.getElementById("camera-select").addEventListener("change", function() {
        var selectedIndex = this.value;  // 获取选中的摄像头索引
        refreshCameraImage(selectedIndex); // 刷新选中的摄像头图像
    });
</script>

</html>
