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
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="../api/car_owner_wait_zone_edit" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">编辑等待区</h2>
            <!-- ID -->
            <div class="form-group">
                <label>等待区ID</label>
                <input type="text" name="id" class="form-control" value="{{data.id}}" readonly>
            </div>

            <!-- 绑定点位 -->
            <div class="form-group">
                <label>绑定点位</label>
                <select class="form-control" name="point_id">
                % for point in points:
                <option value="{{point.id}}" {% if point.id == data.point_id %}selected{% endif %}>{{point.description}}({{point.x}},{{point.y}})</option>
                % end
                </select>
            </div>

            <!-- 等待区名称 -->
            <div class="form-group">
                <label>等待区名称</label>
                <input type="text" name="name" class="form-control" value="{{data.name}}" placeholder="请输入等待区名称" required>
            </div>

            <!-- 描述 -->
            <div class="form-group">
                <label for="description">描述</label>
                <textarea name="description" id="description" class="form-control" rows="4" placeholder="请输入描述" required>{{data.description}}</textarea>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%;">修改</button>
        </form>
    </div>
</body>

</html>
