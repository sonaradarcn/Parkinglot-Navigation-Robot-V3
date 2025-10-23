<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="utf-8">
    <title>Verification Service - Powered by Sonaradar Electronic Inc.</title>
    <style type="text/css">
        *, *:before, *:after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Open Sans', Helvetica, Arial, sans-serif;
            background: #ededed;
        }

        input, button, select {
            border: none;
            outline: none;
            background: none;
            font-family: 'Open Sans', Helvetica, Arial, sans-serif;
        }

        .tip {
            font-size: 20px;
            margin: 40px auto 50px;
            text-align: center;
        }

        .content {
            overflow: hidden;
            position: absolute;
            left: 50%;
            top: 50%;
            width: 900px;
            height: 550px;
            margin: -300px 0 0 -450px;
            background: #fff;
        }

        .form {
            position: relative;

            height: 100%;
            transition: -webkit-transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
            padding: 50px 30px 0;
        }

        .sub-cont {
            overflow: hidden;
            position: absolute;
            left: 640px;
            top: 0;
            width: 900px;
            height: 100%;
            padding-left: 260px;
            background: #fff;
            transition: -webkit-transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
        }

        .content.s--signup .sub-cont {
            -webkit-transform: translate3d(-640px, 0, 0);
            transform: translate3d(-640px, 0, 0);
        }

        button {
            display: block;
            margin: 0 auto;
            width: 260px;
            height: 36px;
            border-radius: 30px;
            color: #fff;
            font-size: 15px;
            cursor: pointer;
        }

        .img {
            overflow: hidden;
            z-index: 2;
            position: absolute;
            left: 0;
            top: 0;
            width: 260px;
            height: 100%;
            padding-top: 360px;
        }

        .img:before {
            content: '';
            position: absolute;
            right: 0;
            top: 0;
            width: 900px;
            height: 100%;
            background-image: url('../static/images/loginBackground_inner.png');
            background-size: cover;
            transition: -webkit-transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
        }

        .img:after {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
        }

        .content.s--signup .img:before {
            -webkit-transform: translate3d(640px, 0, 0);
            transform: translate3d(640px, 0, 0);
        }

        .img__text {
            z-index: 2;
            position: absolute;
            left: 0;
            top: 50px;
            width: 100%;
            padding: 0 20px;
            text-align: center;
            color: #fff;
            transition: -webkit-transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out;
            transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
        }

        .img__text h2 {
            margin-bottom: 10px;
            font-weight: normal;
        }

        .img__text p {
            font-size: 14px;
            line-height: 1.5;
        }

        .content.s--signup .img__text.m--up {
            -webkit-transform: translateX(520px);
            transform: translateX(520px);
        }
        .img__text.m--in {
            -webkit-transform: translateX(-520px);
            transform: translateX(-520px);
        }

        .content.s--signup .img__text.m--in {
            -webkit-transform: translateX(0);
            transform: translateX(0);
        }

        .img__btn {
            overflow: hidden;
            z-index: 2;
            position: relative;
            width: 100px;
            height: 36px;
            margin: 0 auto;
            background: transparent;
            color: #fff;
            text-transform: uppercase;
            font-size: 15px;
            cursor: pointer;
        }
        .img__btn:after {
            content: '';
            z-index: 2;
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            border: 2px solid #fff;
            border-radius: 30px;
        }

        .img__btn span {
            position: absolute;
            left: 0;
            top: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            transition: -webkit-transform 0.6s;
            transition: transform 0.6s;
            transition: transform 0.6s, -webkit-transform 0.6s;
        }

        .img__btn span.m--in {
            -webkit-transform: translateY(-72px);
            transform: translateY(-72px);
        }

        .content.s--signup .img__btn span.m--in {
            -webkit-transform: translateY(0);
            transform: translateY(0);
        }

        .content.s--signup .img__btn span.m--up {
            -webkit-transform: translateY(72px);
            transform: translateY(72px);
        }

        h2 {
            width: 100%;
            font-size: 26px;
            text-align: center;
        }

        label {
            display: block;
            width: 260px;
            margin: 25px auto 0;
            text-align: center;
        }

        label span {
            font-size: 12px;
            color: #909399;
            text-transform: uppercase;
        }

        input {
            display: block;
            width: 100%;
            margin-top: 5px;
            padding-bottom: 5px;
            font-size: 16px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.4);
            text-align: center;
        }

        select {
            display: block;
            width: 100%;
            margin-top: 5px;
            padding-bottom: 5px;
            font-size: 16px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.4);
            text-align: center;
        }

        .forgot-pass {
            margin-top: 15px;
            text-align: center;
            font-size: 12px;
            color: #cfcfcf;
        }

        .forgot-pass a {
            color: #cfcfcf;
        }

        .submit {
            margin-top: 40px;
            margin-bottom: 20px;
            background: #d4af7a;
            text-transform: uppercase;
        }

        .fb-btn {
            border: 2px solid #d3dae9;
            color: #8fa1c7;
        }
        .fb-btn span {
            font-weight: bold;
            color: #455a81;
        }

        .sign-in {
            transition-timing-function: ease-out;
        }
        .content.s--signup .sign-in {
            transition-timing-function: ease-in-out;
            transition-duration: 0.6s;
            -webkit-transform: translate3d(640px, 0, 0);
            transform: translate3d(640px, 0, 0);
        }

        .sign-up {
            -webkit-transform: translate3d(-900px, 0, 0);
            transform: translate3d(-900px, 0, 0);
        }
        .content.s--signup .sign-up {
            -webkit-transform: translate3d(0, 0, 0);
            transform: translate3d(0, 0, 0);
        }
        /* 动画效果 */
        @keyframes slide-in-left2 {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .slide-in-left2 {
            animation: slide-in-left2 2.0s ease;
        }
        .button {
            background-color: #1E90FF;
            color: #FFF;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        .button:hover {
            color: #fff;
            background-color: #00BFFF;
        }
        .button-transparent {
            background-color: transparent;
            color: white;
            border-color: white;
            border-radius: 5px;
            border: 3px solid #ccc;
            transition: all 0.3s ease-in-out;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }
        .button-transparent:hover {
            background-color: #888;
            color: white;
            border-color: #888;
        }
    </style>

</head>

<body style="align-items: center;justify-content: center;display: flex;height: 100vh;background:url('../static/images/background.png');background-size:cover;background-attachment:fixed;background-position: center;overflow-x:hidden;overflow-y:hidden;animation: slide-in-left2 1.0s;" oncontextmenu="return false" onselectstart="return false">
<div class="content" style="border-radius: 7px;box-shadow: 0px 0px 5px 2px rgba(0,0,0,0.1);">
    <div class="form sign-in" style="align-items: center;justify-content: center;display: flex;">
        <div>
            <h2>登录 LOGIN</h2>
            <form action="/api/login" method="get">
                <label>
                    <span style="font-size: 14px;">用户名 USERNAME</span>
                    <input name="username" id="username" type="text" required />
                </label>
                <label>
                    <span style="font-size: 14px;" >密码 PASSWORD</span>
                    <input type="password" name="password" id="password" required/>
                </label>
                <label style="display: flex;justify-content: center;align-items: center;">
                    <input type="checkbox" name="autoLogin" id="autoLogin" style="width: 24px;"/>
                    <span style="font-size: 14px;" >自动登录 AUTO LOGIN</span>
                </label>
                <button type="submit" class="button" style="margin-top: 10px;height: 40px;">登 录</button>
            </form>
        </div>
    </div>
</div>

<form style="position: fixed;bottom: 10px;width: 100%;animation: slide-in-left2 1.0s;min-width: 500px;">
    <div style="padding-top: 40px;animation: slide-in-left 2.0s;">
        <div style="align-items: center;justify-content: center;display: flex;padding-top: 10px">
            <img src="../static/images/logo.png" style="width: 48px;height: 48px;">
            <div style="padding-left: 20px;">
                <div style="text-align: center;font-size: 20px;color: white;text-shadow: 2px 2px 4px #000000; ">Sonaradar Electronic Inc</div>
                <div style="text-align: center;font-size: 8px;color: whitesmoke;text-shadow: 2px 2px 4px #000000;">© 2014-2025 Sonaradar Electronic Inc.All Rights Reserved.</div>
            </div>
        </div>
    </div>
</form>

<div style="position: fixed;bottom: 10px;right: 10px;animation: slide-in-left 1.0s;" hidden>
  <div style="align-items: center;justify-content: center;display: flex;">
    <input class="button-transparent" style="width: 50px;height: 50px;background-image: url('../static/images/back.png');" onclick="window.location.href='#'" value="" type="button"/>
  </div>
</div>

<script>
    document.querySelector('.img__btn').addEventListener('click', function() {
        document.querySelector('.content').classList.toggle('s--signup')
    })
</script>
<style>
    .copyrights{text-indent:-9999px;height:0;line-height:0;font-size:0;overflow:hidden;}
</style>

</body>

</html>
