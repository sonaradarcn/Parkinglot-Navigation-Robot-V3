<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>Sonaradar PNR - Manage Platform</title>

    <link rel="stylesheet" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/font-awesome.css">
    <link rel="stylesheet" href="../static/css/nprogress.css">
    <link rel="stylesheet" href="../static/css/admin.css">


</head>
<body>

<div class="big-wrap">
    <div id="content-wrap" class="content-wrap" >
        <header id="header" class="trans-all-2">
            <button id="drawer-toggle" type="button" class="btn btn-default btn-lg ">
                <i class="fa fa-list " aria-hidden="true"></i>
            </button>
            <!--<div class="login-panel" style="margin-left: auto;">
                <div class="dropdown pull-right">
                    
                    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdown-user">
                        <li role="presentation">
                            <a role="menuitem" tabindex="-1" href="api/user?type=logout">退出</a>
                        </li>
                        <li role="presentation">
                            <a role="menuitem" tabindex="-1" onclick="loadPage('manage_userinfo_changepwd.jsp')">修改密码</a>
                        </li>

                    </ul>
                </div>
            </div>-->
        </header>
        <iframe id="container" class="main-content " src="" style="top:0px;bottom: 0px;border: none;"></iframe>
        <!--<div class="main-content ">
            <iframe id="container" src="manage_index.jsp" style="top:0px;bottom: 0px;border: none;"></iframe>
        </div>-->
    </div>
    <aside id="drawer" class="trans-all-2">
        <div class="drawer-head">
            <i class="logo fa fa-null fa-lg" aria-hidden="true"></i>
            <a href="../page/manage" class="logo-text">设置面板</a>
        </div>

        <ul class="menu-parent menu-root">
            <li class="menu-child" style="background: #08415C">
                <a href="#"
                   class="menu-link"><i class="menu-icon fa fa-null"></i><span class="menu-desc">首页</span></a>
            </li>

            <li class="menu-child">
                <a class="menu-link">
                    <i class="menu-icon fa fa-null"></i>
                    <span class="menu-desc">车位管理</span>
                    <span class="menu-more"><i class="fa fa-chevron-right"></i></span>
                </a>
                <ul class="menu-parent">
                    <li class="menu-child"><a onclick="loadPage('../page/manage_parking_place_list');" class="menu-link">车位管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_cprd_list');" class="menu-link">CPR设备管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_cpri_list');" class="menu-link">CPR信息管理</a></li>
                </ul>
            </li>

            <li class="menu-child">
                <a class="menu-link">
                    <i class="menu-icon fa fa-null"></i>
                    <span class="menu-desc">点位管理</span>
                    <span class="menu-more"><i class="fa fa-chevron-right"></i></span>
                </a>
                <ul class="menu-parent">
                    <li class="menu-child"><a onclick="loadPage('../page/manage_point_list');" class="menu-link">点位管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_parking_place_list');" class="menu-link">车位点位关联管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_car_owner_wait_zone_list');" class="menu-link">车主等待区点位关联管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_robot_standby_position_list');" class="menu-link">机器人待机点位关联管理</a></li>
                </ul>
            </li>

            <li class="menu-child">
                <a class="menu-link">
                    <i class="menu-icon fa fa-null"></i>
                    <span class="menu-desc">机器人管理</span>
                    <span class="menu-more"><i class="fa fa-chevron-right"></i></span>
                </a>
                <ul class="menu-parent">
                    <li class="menu-child"><a onclick="loadPage('../page/manage_robot_list');" class="menu-link">机器人管理</a></li>
                    <li class="menu-child"><a onclick="loadPage('../page/manage_robot_standby_position_list');" class="menu-link">机器人待机点位关联管理</a></li>
                </ul>
            </li>

            <li class="menu-child">
                <a class="menu-link">
                    <i class="menu-icon fa fa-null"></i>
                    <span class="menu-desc">用户管理选项</span>
                    <span class="menu-more"><i class="fa fa-chevron-right"></i></span>
                </a>
                <ul class="menu-parent">
                    <li class="menu-child"><a onclick="loadPage('../page/manage_user_list');" class="menu-link">用户管理</a></li>
                </ul>
            </li>


            <li class="menu-child">
                <a class="menu-link">
                    <i class="menu-icon fa fa-null"></i>
                    <span class="menu-desc">更多选项</span>
                    <span class="menu-more"><i class="fa fa-chevron-right"></i></span>
                </a>
                <ul class="menu-parent">
                    <li class="menu-child"><a onclick="loadPage('../page/dev');" class="menu-link">系统信息</a></li>
                    <li class="menu-child"><a href="/" class="menu-link">退出登录</a></li>
                </ul>
            </li>
        </ul>
    </aside>
</div>

<script type="text/javascript">
    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=")
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1
                c_end = document.cookie.indexOf(";", c_start)
                if (c_end == -1) c_end = document.cookie.length
                return unescape(document.cookie.substring(c_start, c_end))
            }
        }
        return ""
    }

    function setCookie(c_name, value, expiredays) {
        var exdate = new Date()
        exdate.setDate(exdate.getDate() + expiredays)
        document.cookie = c_name + "=" + escape(value) +
            ((expiredays == null) ? "" : "; expires=" + exdate.toGMTString())
    }


    function hasClass(element, Hclass) {
        var patt = new RegExp(Hclass)
        return patt.test(element.className)
    }

    function addClass(element, Hclass) {
        if (!hasClass(element, Hclass)) {
            element.className += ' ' + Hclass;
        }
    }

    function removeClass(element, Hclass) {
        if (hasClass(element, Hclass)) {
            var re = element.className
            re = re.replace(Hclass, '');
            element.className = re
        }
    }

    //保证关闭了侧拉栏之后，刷新浏览器测拉栏不会跑出来，为了减少卡顿，使用原生
    if(getCookie('drawerIsClosed')){
        addClass(document.getElementById('drawer'),'drawer-closed')
        addClass(document.getElementById('content-wrap'),'content-wrap-full')
    }

</script>
<!--import script-->
<script type="application/javascript" src="../static/js/jquery.min.js"></script>
<script type="application/javascript" src="../static/js/jquery.pjax.js"></script>
<script type="application/javascript" src="../static/js/bootstrap.js"></script>
<script type="application/javascript" src="../static/js/nprogress.js"></script>
<script>
    $(function () {
        // 抽屉按钮
        $('#drawer-toggle').on('click', function () {
            $('#drawer').toggleClass('drawer-closed')

            if ($('#drawer').hasClass('drawer-closed')) {
                setCookie('drawerIsClosed', true, 365);
                $('.content-wrap').addClass('content-wrap-full')
            } else {
                setCookie('drawerIsClosed', '', 365);
                $('.content-wrap').removeClass('content-wrap-full')
            }
        });

        // 抽屉菜单控制
        $('#drawer .menu-link').on('click', function (e) {
            var $t = $(this);
            var $item = $t.parent('.menu-child')
            var nextPar = $item.children('.menu-parent');

            if(nextPar.length){
                if($item.hasClass('open')){
                    $item.children('.menu-parent').stop(false,true).slideUp(200)
                    $item.removeClass('open')
                }else{
                    $('#drawer .open').removeClass('open').children('.menu-parent').stop(false,true).slideUp(200)
                    $item.addClass('open')
                    $item.children('.menu-parent').stop(false,true).slideDown(200)
                }
            }else{
                $('#drawer .open').not($t.parents('.menu-child'))
                    .removeClass('open')
                    .children('.menu-parent')
                    .stop(false,true).slideUp(200)
            }

        });
    });
    function loadPage(url) {
        document.getElementById("container").src = url;
    }
</script>
</body>
</html>

