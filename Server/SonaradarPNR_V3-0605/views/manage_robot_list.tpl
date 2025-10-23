<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Robot Management</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加机器人" onclick="window.location='../page/manage_robot_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>机器码</th>
            <th>名称</th>
            <th>描述</th>
            <th>模式</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for robot in data:
            <tr>
                <td>{{ robot.id }}</td>
                <td>{{ robot.machine_id }}</td>
                <td>{{ robot.name }}</td>
                <td>{{ robot.description }}</td>
                % if robot.mode == 1:
                <td>服务模式</td>
                % elif robot.mode == 2:
                <td>调试模式</td>
                % elif robot.mode == 0:
                <td>暂停服务</td>
                % end

                % flag = False
                % for availableRobot in availableRobotsData:
                % if availableRobot.id == robot.id:
                <td style="color:#1db808;font-weight: 600;">在线</td>
                % flag = True
                % break
                % end
                % end

                % if flag == False:
                <td style="color:#e00101;font-weight: 600;">离线</td>
                % end

                <td>
                    <a style="color: #8c8c8c; text-decoration: none;" href="../page/manage_robot_edit?id={{ robot.id }}">编辑</a>
                    <a style="color: #8c8c8c; text-decoration: none; padding-left: 10px;" href="../api/robot_remove?id={{ robot.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
