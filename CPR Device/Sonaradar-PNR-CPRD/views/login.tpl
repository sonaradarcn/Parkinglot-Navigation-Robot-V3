<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sonaradar-CPRD 设备访问认证</title>
    <style>
        /* 设置页面背景图 */
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: url('../static/images/background.png') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
			overflow: hidden;
        }

        /* 登录框的滑动效果 */
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 1000px;
            animation: slide-in-up 1s ease-out, fade-in 1s ease-out;
        }

        /* 盒子渐变出现 */
        @keyframes fade-in {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        /* 自下而上的滑动动画 */
        @keyframes slide-in-up {
            0% {
                transform: translateY(100%);
                opacity: 0;
            }
            100% {
                transform: translateY(0);
                opacity: 1;
            }
        }

        /* 白色登录框样式 */
        .login-box {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 100%;
        }

        h2 {
            margin-bottom: 20px;
            font-size: 24px;
        }

        /* 输入框样式 */
        .input-field {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            outline: none;
            transition: border 0.3s, box-shadow 0.3s;
        }

        /* 输入框底部蓝色 */
        .input-field:focus {
            border-bottom: 3px solid #2196F3;
            box-shadow: 0 2px 10px rgba(33, 150, 243, 0.4);
        }

        /* 登录按钮样式 */
        .login-button {
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #2196F3, #87CEFA);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }

        /* 按钮悬浮效果 */
        .login-button:hover {
            background: linear-gradient(135deg, #87CEFA, #2196F3);
            transform: scale(1.05);
        }

        /* 按钮点击效果 */
        .login-button:active {
            transform: scale(0.98);
        }

        /* 底部版权信息浮现效果 */
        @keyframes fade-in-bottom {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* 固定底部版权信息样式 */
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            animation: fade-in-bottom 2s ease-out;
            min-width: 500px;
            text-align: center;
        }

        /* 中央文本样式 */
        .footer img {
            width: 48px;
            height: 48px;
        }

        .footer div {
            color: white;
            text-shadow: 2px 2px 4px #000000;
        }

        .footer .footer-text {
            font-size: 20px;
        }

        .footer .footer-small {
            font-size: 8px;
            color: whitesmoke;
            font-weight: bold;
        }

    </style>
</head>
<body oncontextmenu="return false" onselectstart="return false">
    <div class="login-container">
        <div class="login-box" style="align-items: center;justify-content: center;display: flex;">
            <div style="width: 50%;padding-top: 100px;padding-bottom: 100px">
                <h2>Sonaradar-CPRD 设备访问认证</h2>
                <form action="../api/login" method="GET">
                    <div style="text-align: left;margin-left: 2px">用户名</div>
                    <input type="text" class="input-field" name="username" placeholder="用户名" required><br>
                    <div style="text-align: left">密码</div>
                    <input type="password" class="input-field" name="password" placeholder="密码" required><br>
                    <div style="align-items: center;justify-content: center;display: flex;">
                        <button type="submit" style="width: 60%;margin-top: 20px;" class="login-button">登录</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div class="footer">
        <div style="padding-top: 40px;">
            <div style="align-items: center;justify-content: center;display: flex;padding-top: 10px">
                <img src="../static/images/logo.png">
                <div style="padding-left: 20px;">
                    <div class="footer-text">Sonaradar Electronic Inc</div>
                    <div class="footer-small">© 2014-2025 Sonaradar Electronic Inc. All Rights Reserved.</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
