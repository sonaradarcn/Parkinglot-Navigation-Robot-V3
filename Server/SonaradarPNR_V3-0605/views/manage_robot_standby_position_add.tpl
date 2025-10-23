<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>添加机器人备用位置</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
    <div class="container mt-5" style="align-items: center; justify-content: center; display: flex;">
        <form action="../api/robot_standby_position_add" method="get" style="width: 700px; margin-top: 20px; margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加机器人待机位置</h2>

            <div class="form-group">
                <label for="name">待机位置名称</label>
                <input type="text" name="name" id="name" class="form-control" value="" placeholder="请输入位置名称" required>
            </div>

            <div class="form-group">
                <label for="description">待机位置描述</label>
                <textarea name="description" id="description" class="form-control" rows="3" placeholder="请输入位置描述" required></textarea>
            </div>

            <div class="form-group">
                <label>绑定机器人</label>
                <select class="form-control" name="robot_id">
                    % for robot in robots:
                    <option value="{{robot.id}}">{{robot.name}}(MID:{{robot.machine_id}})</option>
                    % end
                </select>
            </div>

            <div class="form-group">
                <label>绑定点位</label>
                <select class="form-control" name="point_id">
                    % for point in points:
                    <option value="{{point.id}}">{{point.description}}({{point.x}},{{point.y}})</option>
                    % end
                </select>
            </div>



            <button type="submit" class="btn btn-primary" style="width: 100%;">添 加</button>
        </form>
    </div>
</body>
</html>
