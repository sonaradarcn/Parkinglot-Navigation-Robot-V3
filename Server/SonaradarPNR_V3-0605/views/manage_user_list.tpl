<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>admin</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加用户" onclick="window.location='../page/manage_user_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>UID</th>
            <th>用户名称</th>
            <th>用户类别</th>
            <th>用户状态</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for user in data:
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                % if user.role == 2:
                <td>超级管理员</td>
                % else:
                <td>管理员</td>
                % end
                % if user.enable == 1:
                <td style="color:#1db808;font-weight: 600;">启用</td>
                % else:
                <td style="color:#e00101;font-weight: 600;">禁用</td>
                % end
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_user_edit?id={{ user.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/user_remove?id={{ user.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
