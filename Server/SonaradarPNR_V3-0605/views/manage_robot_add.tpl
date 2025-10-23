<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>添加机器人</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<body>
    <div class="container mt-5" style="align-items: center; justify-content: center; display: flex;">
        <form action="../api/robot_add" method="get" style="width: 700px; margin-top: 20px; margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加机器人</h2>
            <div class="form-group">
                <label>机器码</label>
                <input type="text" name="machine_id" class="form-control" value="" placeholder="请输入机器码">
            </div>
            <div class="form-group">
                <label>机器人名称</label>
                <input type="text" name="name" class="form-control" value="" placeholder="请输入机器人名称">
            </div>
            <div class="form-group">
                <label>机器人描述</label>
                <textarea name="description" class="form-control" placeholder="请输入机器人描述"></textarea>
            </div>
            <div class="form-group">
                <label>机器人模式</label>
                <select class="form-control" name="mode">
                    <option value="1" selected>服务模式</option>
                    <option value="2">调试模式</option>
                    <option value="0">暂停服务</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">添 加</button>
        </form>
    </div>
</body>

</html>
