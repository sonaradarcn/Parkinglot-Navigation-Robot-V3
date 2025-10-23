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
        <form action="../api/user_add" method="get" style="width: 700px;margin-top: 20px;margin-bottom: 20px;" class="fadeIn animated">
            <h2 class="text-center mb-4">添加用户</h2>
            <div class="form-group" type="">
                <label>用户名</label>
                <input type="text" name="username" class="form-control" value=""
                    placeholder="请输入用户名" >
            </div>
            <div class="form-group" type="">
                <label>密码</label>
                <input type="text" name="password" class="form-control" value="" placeholder="请输入密码">
            </div>
            <div class="form-group" type="">
                <label>用户类别</label>
                <select class="form-control" name="role">
                    <option value="1" selected>管理员</option>
                    <option value="2">超级管理员</option>
                </select>
            </div>
            <div class="form-group" type="">
                <label>用户状态</label>
                <select class="form-control" name="enable">
                    <option value="1" selected>启用</option>
                    <option value="0">禁用</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">添 加</button>
        </form>
    </div>
</body>

</html>