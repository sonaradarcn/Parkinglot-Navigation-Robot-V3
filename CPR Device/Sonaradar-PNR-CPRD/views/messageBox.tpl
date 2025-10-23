<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="utf-8">
    <title>提示</title>
</head>
<!--<script>-->
<!--    alert('{{message}}');-->
<!--    window.location='{{redirectURL}}';-->
<!--</script>-->
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>admin</title>
    <link rel="stylesheet" type="text/css" href="../static/css/SonaradarBlueOcean.css">
    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body style="align-items: center;justify-content: center;display: flex;height: 100vh;background-size:cover;background-attachment:fixed;background-position: center;overflow-x:hidden;overflow-y:hidden;" onselectstart="return false" >
    <div class="container" style="align-items: center;justify-content: center;display: flex;width: 900px;height: 400px;background-color: white">
    <div>
        <div style="display: flex;justify-content: center">
            <image src="../static/images/info.png" style="width:72px;height:72px"></image>
        </div>
        <div style="display: flex;justify-content: center;">
            <label style="font-size: 28px;font-weight: bold;margin-top: 20px;text-align: center">提示</label>
        </div>
        <div style="display: flex;justify-content: center;margin-top: 20px">
            <label style="color: #767676;font-size: 24px;font-weight: bold;letter-spacing: 1px;text-align: center">{{message}}</label>
        </div>
        <div style="display: flex;justify-content: center;margin-top: 40px;width: 100%">
            <input type="button" class="button" style="height: 50px;font-size: 20px;font-weight: bold;letter-spacing: 2px;width: 100%" value="确认" onclick="window.location ='{{redirectURL}}';"/>
        </div>

    </div>
</div>
</body>