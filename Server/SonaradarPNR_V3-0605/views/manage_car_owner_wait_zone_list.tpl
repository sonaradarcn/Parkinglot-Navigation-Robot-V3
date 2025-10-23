<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>Car Owner Wait Zone Management</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加等待区" onclick="window.location='../page/manage_car_owner_wait_zone_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>等待区名称</th>
            <th>关联地点</th>
            <th>描述</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for car_owner_wait_zone in data:
            <tr>
                <td>{{ car_owner_wait_zone.id }}</td>
                <td>{{ car_owner_wait_zone.name }}</td>
                <td>{{ car_owner_wait_zone.point_id_in_point }} </td>
                <td>{{ car_owner_wait_zone.description }}</td>
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_car_owner_wait_zone_edit?id={{ car_owner_wait_zone.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/car_owner_wait_zone_remove?id={{ car_owner_wait_zone.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
