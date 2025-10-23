<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>CPRDevice 管理</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加设备" onclick="window.location='../page/manage_cprd_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>机器码</th>
            <th>名称</th>
            <th>描述</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % flag = False
            % for device in data:
                % for availableCPRDevice in availableCPRDeviceData:
                % if availableCPRDevice.id == device.id:
            <tr>
                <td>{{ device.id }}</td>
                <td>{{ device.machine_id }}</td>
                <td>{{ device.name }}</td>
                <td>{{ device.description }}</td>
                <td style="color:#1db808;font-weight: 600;">在线</td>
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_cprd_edit?id={{ device.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;" href="http://{{availableCPRDevice.description}}:8080/">跳转到设备管理页面</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/cprd_remove?id={{ device.id }}">删除</a>
                </td>
            </tr>
                % flag = True
                % break
                % end
                % end
            % if flag == False:
            <tr>
                <td>{{ device.id }}</td>
                <td>{{ device.machine_id }}</td>
                <td>{{ device.name }}</td>
                <td>{{ device.description }}</td>
                <td style="color:#e00101;font-weight: 600;">离线</td>
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_cprd_edit?id={{ device.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/cprd_remove?id={{ device.id }}">删除</a>
                </td>
            </tr>
            % end
            % end
        </tbody>
    </table>
</div>
</body>
</html>
