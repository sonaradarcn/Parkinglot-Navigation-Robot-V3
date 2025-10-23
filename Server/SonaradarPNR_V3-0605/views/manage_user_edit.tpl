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
        <form action="../api/user_edit" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">修改用户信息</h2>
            <div class="form-group" type="">
                <label>UID</label>
                <input type="text" name="id" class="form-control" value="{{data.id}}"
                    placeholder="" readonly>
            </div>
            <div class="form-group" type="">
                <label>用户名</label>
                <input type="text" name="username" class="form-control" value="{{data.username}}"
                    placeholder="请输入用户名" required>
            </div>
            <div class="form-group" type="">
                <label>密码</label>
                <input type="text" name="password" class="form-control" value="{{data.password}}" placeholder="请输入密码" required>
            </div>
            <div class="form-group" type="">
                <label>用户类别</label>
                <select class="form-control" name="role">
                    % if data.role == 1:
                    <option value="1" selected>管理员</option>
                    <option value="2">超级管理员</option>
                    % else:
                    <option value="1">管理员</option>
                    <option value="2" selected>超级管理员</option>
                    % end
                </select>
            </div>
            <div class="form-group" type="">
                <label>用户状态</label>
                <select class="form-control" name="enable">
                    % if data.enable == 0:
                    <option value="1">启用</option>
                    <option value="0" selected>禁用</option>
                    % else:
                    <option value="1" selected>启用</option>
                    <option value="0">禁用</option>
                    %end
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">修 改</button>
        </form>
    </div>
</body>

</html>