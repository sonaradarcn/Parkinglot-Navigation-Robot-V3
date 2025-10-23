<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录界面</title>
    <link rel="stylesheet" href="../static/css/SonaradarOceanBlueV2.css"> <!-- 引入外部CSS文件 -->
</head>
<!-- <script>


    // 页面加载时启动定时器
    window.onload = function () {
        // 设置定时器，延迟 5 秒后执行播放音频操作
        setTimeout(function () {
            // 设置 step_name 参数（你可以根据实际需要修改这个值）
            const stepName = 'step_off_service'; // 这里的 step_name 可以动态设置

            // 使用 fetch 发送请求，并携带 step_name 参数
            fetch(`../api/turn_next_page?step_name=${encodeURIComponent(stepName)}`) // 假设后台接口是 '/check_condition'
                .then(response => response.json())  // 解析后台返回的 JSON
                .then(data => {
                    if (data.redirectUrl) {
                        // 如果后台返回了新页面的地址，则跳转到该页面
                        window.location.href = data.redirectUrl;
                    } else {
                        // 如果没有返回跳转地址，设置下次请求
                        setTimeout(pollBackend, 1000); // 1秒后再次轮询
                    }
                })
                .catch(error => {
                    console.error('请求出错:', error);
                    // 如果请求出错，设置下次请求
                    setTimeout(pollBackend, 5000); // 1秒后再次轮询
                });
        }, 1000); // 延迟 5000 毫秒（5 秒）后播放音频
    };
</script> -->
<script>
    // 步骤名称
function step_name() {
    // 轮询后台的函数
    function pollBackend() {
        // 设置 step_name 参数（你可以根据实际需要修改这个值）
        const stepName = 'step_off_service'; // 这里的 step_name 可以动态设置
        
        // 使用 fetch 发送请求，并携带 step_name 参数
        fetch(`../api/turn_next_page?step_name=${encodeURIComponent(stepName)}`) // 假设后台接口是 '/check_condition'
            .then(response => response.json())  // 解析后台返回的 JSON
            .then(data => {
                if (data.redirectUrl) {
                    // 如果后台返回了新页面的地址，则跳转到该页面
                    window.location.href = data.redirectUrl;
                } else {
                    // 如果没有返回跳转地址，设置下次请求
                    setTimeout(pollBackend, 1000); // 1秒后再次轮询
                }
            })
            .catch(error => {
                console.error('请求出错:', error);
                // 如果请求出错，设置下次请求
                setTimeout(pollBackend, 1000); // 1秒后再次轮询
            });
    }

    // 初次调用轮询
    pollBackend();
}
// 调用 step_name 函数启动轮询
step_name();
</script>


<body>
    <div class="left-side"></div>
    <div class="right-side">
        <div class="form-container">
            <div style='align-items: center;justify-content: center;display: flex;'>
                <img src="../static/images/stop.png" style="width: 72px;height: 72px;border-radius: 2px;">
            </div>
            <h2 style="letter-spacing: 2px;font-size: 24px;">暂停服务</h2>
            <div style="font-size: 20px;text-align: center;line-height: 30px;font-weight: 600">
                本机已暂停服务<br />请您使用其他机器人寻车
            </div>
        </div>
    </div>
    <div style="position: fixed;left: 10px;bottom: 10px;animation: slide-in-left 1.0s;display: flex">
        <img src="../static/images/logo.png" style="width: 48px;height: 48px;border-radius: 2px;">
        <div style="padding-left: 10px;padding-top: 4px;">
            <div style="font-size: 24px;color: #ffffff;text-shadow: 1px 1px 2px #000000;">Machine ID:{{machine_id}}
            </div>
            <div style="font-size: 14px;color: #ffffff;text-shadow: 1px 1px 2px #000000;">© 2023-2025 Sonaradar
                Electronic Inc. All Rights Reserved.</div>
        </div>
    </div>
</body>

</html>