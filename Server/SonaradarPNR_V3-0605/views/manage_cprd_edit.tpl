<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>修改CPR设备信息</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<body>
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="../api/cprd_edit" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">修改CPR设备信息</h2>
            <div class="form-group" type="">
                <label>设备ID</label>
                <input type="text" name="id" class="form-control" value="{{data.id}}"
                    placeholder="" readonly>
            </div>
            <div class="form-group" type="">
                <label>机器编号</label>
                <input type="text" name="machine_id" class="form-control" value="{{data.machine_id}}"
                    placeholder="请输入机器编号" required>
            </div>
            <div class="form-group" type="">
                <label>设备名称</label>
                <input type="text" name="name" class="form-control" value="{{data.name}}" placeholder="请输入设备名称" required>
            </div>
            <div class="form-group" type="">
                <label>设备描述</label>
                <textarea class="form-control" name="description" rows="4" placeholder="请输入设备描述">{{data.description}}</textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">修 改</button>
        </form>
    </div>
</body>

</html>
