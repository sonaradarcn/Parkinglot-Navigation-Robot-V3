<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CPR信息管理</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>
<body>
<div id="container" class="main-content container">
    <ul class="list-unstyled" style="margin-top: 20px;">
        <input type="button" class="btn btn-primary" value="添加CPR信息" onclick="window.location='../page/manage_cpri_add';" />
    </ul>

    <table style="margin-top: 20px;" class="table table-bordered table-hover table-responsive">
        <thead>
        <tr style="height: 30px;">
            <th>ID</th>
            <th>区域名称</th>
            <th>描述</th>
            <th>绑定CPRD信息</th> <!-- 添加 CPRD ID 列 -->
            <th>车牌号</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        </thead>
        <tbody>
            % for cpri in data:
            <tr>
                <td>{{ cpri.id }}</td>
                <td>{{ cpri.name }}</td>
                <td>{{ cpri.description }}</td>
                % for cprd in cprdData:
                % if cpri.cprd_id == cprd.id:
                <td>{{cprd.name}}(MID:{{cprd.machine_id}})</td> <!-- 显示 CPRD ID -->
                % break
                % end
                % end
                <td>{{ cpri.car_plate_no }}</td>
                % if cpri.occupying_flag == 1:
                <td style="color:#e00101;font-weight: 600;">占用</td>
                % else:
                <td style="color:#1db808;font-weight: 600;">空闲</td>
                % end
                <td>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_cpri_edit?id={{ cpri.id }}">编辑</a>
                    <a style="color: #8c8c8c;text-decoration: none;" href="../page/manage_cpri_view?id={{ cpri.id }}">查看详情</a>
                    <a style="color: #8c8c8c;text-decoration: none;padding-left: 10px;" href="../api/cpri_remove?id={{ cpri.id }}">删除</a>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>
</body>
</html>
