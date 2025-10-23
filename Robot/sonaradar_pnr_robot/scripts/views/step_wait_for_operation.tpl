<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录界面</title>
    <link rel="stylesheet" href="../static/css/SonaradarOceanBlueV2.css"> <!-- 引入外部CSS文件 -->
    <script>
        // 定义倒计时的初始时间（单位：秒）
        let remainingTime = 30;

        // 创建一个定时器来更新倒计时
        function startCountdown() {
            // 获取显示剩余时间的元素
            const timeDisplay = document.getElementById("countdown-time");
            const secondDisplay = document.getElementById("countdown-seconds");

            // 更新倒计时显示
            const timer = setInterval(function () {
                // 更新秒数显示
                timeDisplay.textContent = remainingTime;
                secondDisplay.textContent = "秒";

                // 当倒计时结束时，清除定时器
                if (remainingTime <= 0) {
                    clearInterval(timer);
                    // 倒计时结束后，不再更新时间
                    timeDisplay.textContent = 0;
                    secondDisplay.textContent = "秒";
                } else {
                    remainingTime--;
                }
            }, 1000); // 每秒更新一次

        }

        // 页面加载时开始倒计时
        window.onload = startCountdown;
        // 创建音频对象
        var audio = new Audio('../static/audio/notice_wait_for_operation.mp3'); // 替换为实际的 MP3 文件 URL
        audio.autoplay = true; // 自动播放
        audio.play().catch(function (error) {
            console.error('音频播放失败:', error);
        });
        // 轮询后台的函数
        function pollBackend() {
            // 设置 step_name 参数（你可以根据实际需要修改这个值）
            const stepName = 'step_wait_for_operation'; // 这里的 step_name 可以动态设置

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
    </script>

</head>

<body>
    <div class="left-side"></div>
    <div class="right-side">
        <div class="form-container">
            <div style="align-items: center;justify-content: center;display: flex;">
                <!-- 显示倒计时的数字 -->
                <h2 id="countdown-time" style="letter-spacing: 2px;font-size: 72px;padding-top: 20px;color: #00b5e2;">30
                </h2>
                <h2 id="countdown-seconds"
                    style="letter-spacing: 2px;font-size: 24px;padding-top: 20px;color: #00b5e2;padding-left: 10px;padding-top: 80px;">
                    秒</h2>
            </div>
            <h2 style="letter-spacing: 2px;font-size: 24px;">剩余等待时间</h2>
            <div style="font-size: 20px;text-align: center;line-height: 30px;font-weight: 600">
                请您在上述时间内确认寻找车辆<br />超时仍未确认请重新扫码进行操作
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