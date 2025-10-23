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
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="../api/parking_place_add" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加停车位</h2>
            <div class="form-group">
                <label>停车位名称</label>
                <input type="text" name="name" class="form-control" value="" placeholder="请输入停车位名称" required>
            </div>
            <div class="form-group">
                <label>停车位描述</label>
                <input type="text" name="description" class="form-control" value="" placeholder="请输入停车位描述" required>
            </div>
            <div class="form-group">
                <label>识别区绑定</label>
                <select class="form-control" name="cpri_id">
                    % for cpri in cpris:
                    <option value="{{cpri.id}}">{{cpri.name}}(描述:{{cpri.description}})</option>
                    % end
                </select>
            </div>
            <div class="form-group">
                <label>点位绑定</label>
                <select class="form-control" name="point_id">
                    % for point in points:
                    <option value="{{point.id}}">{{point.description}}({{point.x}},{{point.y}})</option>
                    % end
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">添加停车位</button>
        </form>
    </div>
</body>

</html>
