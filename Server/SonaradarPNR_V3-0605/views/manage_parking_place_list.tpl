<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>Parking Place Management</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加停车位" onclick="window.location='../page/manage_parking_place_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>停车位ID</th>
            <th>停车位名称</th>
            <th>停车位描述</th>
            <th>识别区域信息</th>
            <th>点位信息</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for parking_place in data:
            <tr>
                <td>{{ parking_place.id }}</td>
                <td>{{ parking_place.name }}</td>
                <td>{{ parking_place.description }}</td>
                <td>{{ parking_place.cpri_name }}(描述:{{parking_place.cpri_description}})</td>
                <td>{{ parking_place.point_description }}({{parking_place.point_x}},{{parking_place.point_y}})</td>
                % if parking_place.occupying_flag == 1:
                <td style="color:#e00101;font-weight: 600;">占用<label style="color:#000000;font-weight: 600;">(车牌号:{{parking_place.car_plate_no}})</label></td>
                % else:
                <td style="color:#1db808;font-weight: 600;">空闲</td>
                % end
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_parking_place_edit?id={{ parking_place.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/parking_place_remove?id={{ parking_place.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
