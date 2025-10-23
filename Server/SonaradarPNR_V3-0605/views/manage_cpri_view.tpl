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
    <div class="container mt-5" style="align-items: center;justify-content: center;display: flex;">
        <form action="" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">识别区域查看</h2>
            <div class="form-group">
                <label>ID</label>
                <input type="text" name="id" class="form-control" value="{{data.id}}" readonly>
            </div>

            <div class="form-group">
                <label>区域名称</label>
                <input type="text" name="name" class="form-control" value="{{data.name}}" placeholder="请输入区域名称" required readonly>
            </div>

            <div class="form-group">
                <label>描述</label>
                <input type="text" name="description" class="form-control" value="{{data.description}}" placeholder="请输入描述" required readonly>
            </div>

            <!-- 不可修改字段：占用状态，车牌号，图片 -->
            <div class="form-group">
                <label>占用状态</label>
                % if data.occupying_flag == True:
                <input type="text" class="form-control" value="占用" readonly>
                % else:
                <input type="text" class="form-control" value="空闲" readonly>
                % end
            </div>
            % if data.occupying_flag == True:
            <div class="form-group">
                <label>车牌号</label>
                <input type="text" class="form-control" value="{{data.car_plate_no}}" readonly>
            </div>
            % end
            <div class="form-group">
                <label>识别区域图像</label>
                <div id="image-container" style="width: 100%; background-color: #f0f0f0; text-align: center; position: relative;">
                    <img id="image" src="data:image/png;base64,{{image_base64}}" alt="图片" style="width: 100%;" />
                </div>
            </div>

            <button onclick="window.history.back()" class="btn btn-primary" style="width: 100%;">返 回</button>
        </form>
    </div>

</body>

</html>
