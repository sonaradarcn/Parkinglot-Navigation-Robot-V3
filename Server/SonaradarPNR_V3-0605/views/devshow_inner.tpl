<!doctype html>
<html>
<head>
    <meta http-equiv="refresh" content="5">
    <meta charset="utf-8">
    <title>findC</title>
    <link rel="stylesheet" type="text/css" href="../static/css/SonaradarBlueOcean.css">
</head>
<body style="background-color: transparent;align-items: center;justify-content: center;display: flex;height: 100vh;background-size:cover;background-attachment:fixed;background-position: center;overflow-x:hidden;overflow-y:hidden;" onselectstart="return false" >
<div class="container" style="align-items: center;justify-content: center;display: flex;width:900px;height: 500px;background-color: white">
    <div>

        <div>
            <div style="font-size: 32px;font-weight: bold;text-align: center">Sonaradar PNR Project<div style="font-size: 22px;color: #9B9B9B;font-weight: normal;">Get all project at <label onclick="window.location='https://github.com/sonaradar'">https://github.com/sonaradar</label></div></div>
            <div style="font-size: 18px;text-align: center;padding-top: 10px">
                <div>Version: {{version}}</div>

            </div>
            <div id="devFrame" style="align-items: center;justify-content: center;display: flex;padding-top: 40px;animation: slide-in-left2 2.0s;">
                <img src="{{head}}" style="width: 96px;height:96px;border-radius: 48px;box-shadow: 0px 0px 5px 2px rgba(0,0,0,0.1);">
                <div style="padding-left: 20px;">
                    <div style="font-weight: bold;font-size: 24px;">{{description}}</div>
                    <div style="font-size: 22px;padding-top: 5px;">{{nick}}</div>
                    <div style="color: #7A7A7A;font-size: 18px;font-weight: lighter;padding-top: 5px;">@{{name}}</div>
                </div>
            </div>
            <div style="padding-top: 40px;animation: slide-in-left 2.0s;">
                <div style="text-align: center;font-size: 20px;font-weight: bold;">POWERED BY</div>
                <div style="align-items: center;justify-content: center;display: flex;padding-top: 10px">
                    <img src="../static/images/logo.png" style="width: 64px;height: 64px;">
                    <div style="padding-left: 20px;">
                        <div style="text-align: center;font-size: 24px;">Sonaradar Electric LLC</div>
                        <div style="text-align: center;font-size: 12px;color: #9B9B9B">© 2014-2025 Sonaradar Electric LLC.<br/>This project uses GPL-3.0 license.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
