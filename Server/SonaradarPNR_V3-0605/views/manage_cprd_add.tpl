<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>添加CPR设备</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<body>
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="../api/cprd_add" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加CPR设备</h2>
            <div class="form-group" type="">
                <label>机器编号</label>
                <input type="text" name="machine_id" class="form-control" value=""
                    placeholder="请输入机器编号">
            </div>
            <div class="form-group" type="">
                <label>设备名称</label>
                <input type="text" name="name" class="form-control" value="" placeholder="请输入设备名称">
            </div>
            <div class="form-group" type="">
                <label>设备描述</label>
                <textarea class="form-control" name="description" rows="4" placeholder="请输入设备描述"></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">添 加</button>
        </form>
    </div>
</body>

</html>
