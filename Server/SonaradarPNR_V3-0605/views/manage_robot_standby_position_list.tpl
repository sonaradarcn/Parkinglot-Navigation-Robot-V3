<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Robot Standby Position Management</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加机器人待机位置" onclick="window.location='../page/manage_robot_standby_position_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>待机位置名称</th>
            <th>描述</th>
            <th>机器人信息</th>
            <th>点位信息</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for rsp in data:
            <tr>
                <td>{{ rsp.id }}</td>
                <td>{{ rsp.name }}</td>
                <td>{{ rsp.description }}</td>
                <td>{{ rsp.robot_name }}(MID:{{rsp.robot_machine_id}})</td>
                <td>{{rsp.point_description}}({{ rsp.point_x }},{{ rsp.point_y }})</td>
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_robot_standby_position_edit?id={{ rsp.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/robot_standby_position_remove?id={{ rsp.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
