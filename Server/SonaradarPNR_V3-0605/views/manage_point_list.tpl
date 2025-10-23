<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>Point 管理</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加点" onclick="window.location='../page/manage_point_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>坐标 X</th>
            <th>坐标 Y</th>
            <th>描述</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for point in data:
            <tr>
                <td>{{ point.id }}</td>
                <td>{{ point.x }}</td>
                <td>{{ point.y }}</td>
                <td>{{ point.description }}</td>
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_point_edit?id={{ point.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/point_remove?id={{ point.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
