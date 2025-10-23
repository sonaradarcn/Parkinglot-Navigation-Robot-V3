<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>添加点</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">
</head>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    $(document).ready(function() {
        // 为按钮绑定点击事件
        $("#getPositionBtn").click(function() {
            // 获取选中的机器人的ID
            var selectedRobotId = $("#robot").val();

            // 检查是否选择了有效的机器人
            if (!selectedRobotId) {
                alert("请先选择一个机器人！");
                return;
            }

            // 发送 AJAX 请求到 /api/get_robot_position
            $.ajax({
                url: "../api/get_robot_position",  // API URL
                type: "GET",
                data: { id: selectedRobotId },    // 传递机器人ID
                success: function(response) {
                    // 成功处理响应，可以在这里显示返回的数据
                    console.log("机器人位置数据:", response);

                    // 假设 response.x 和 response.y 是返回的坐标数据
                    var x = response.x;
                    var y = response.y;

                    // 检查是否是有效的数字
                    if (isNaN(x) || isNaN(y)) {
                        alert("机器人位置数据无效！");
                        return;
                    }

                    // 将坐标显示在对应的文本框内
                    $("#x").val(x.toFixed(2)); // 显示 X 坐标
                    $("#y").val(y.toFixed(2)); // 显示 Y 坐标
                },
                error: function(xhr, status, error) {
                    // 错误处理
                    console.log("请求失败:", error);
                    alert("获取机器人位置失败，请稍后再试！");
                }
            });
        });
    });
</script>


<body>
    <div class="container mt-5" style="align-items: center; justify-content: center; display: flex;">
        <form action="../api/point_add" method="get" style="width: 700px; margin-top: 20px; margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加点</h2>
            <div class="form-group">
                <label>点位回传机器人选择</label>
                <select class="form-control" name="robot" id="robot">
                    % for availableRobot in availableRobotsData:
                    <option value="{{availableRobot.id}}" selected>{{availableRobot.name}}(MID:{{availableRobot.machine_id}})</option>
                    % end
                </select>
            </div>
            <button type="button" class="btn btn-primary" style="width: 100%;margin-bottom: 10px;" id="getPositionBtn">回传当前选定机器人实时点位</button>
<div class="form-group">
    <label for="x">坐标 X</label>
    <input type="text" name="x" id="x" class="form-control" value="" placeholder="请输入坐标或使用坐标自动回传功能" required>
</div>
<div class="form-group">
    <label for="y">坐标 Y</label>
    <input type="text" name="y" id="y" class="form-control" value="" placeholder="请输入坐标或使用坐标自动回传功能" required>
</div>
            <div class="form-group">
                <label for="description">描述</label>
                <textarea name="description" id="description" class="form-control" rows="3" placeholder="请输入描述"></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">添加</button>
        </form>
    </div>
</body>

</html>
