<!doctype html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <title>Interactive base map</title>
    <link rel="stylesheet" type="text/css" href="https://js.api.here.com/v3/3.1/mapsjs-ui.css" />
    <link rel="stylesheet" type="text/css" href="/assets/css/style.css?get=<?=time()?>" />
    <link rel="stylesheet" type="text/css" href="/assets/css/map.css?get=<?=time()?>" />
</head>
<body id="markers-on-the-map">
    <header>
        <div class="container">
            <div class="logo">impostershop</div>
            <div class="search">
                <input class="search-input" placeholder="Поиск...">
            </div>
            <div class="nav">
                <div class="profile"><img src="/assets/img/profile.png" alt="профиль"></div>
                <div class="basket"><img src="/assets/img/basket.png" alt="корзина"></div>
            </div>
        </div>
    </header>
    <main>
        <div class="banner">
            <img class="img" src="/assets/img/26250.png" alt="картинка">
        </div>
        <div id="map" class="map"></div>
    </main>
    <footer><span>TulaHack2020</span></footer>
    <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-core.js"></script>
    <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-service.js"></script>
    <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-ui.js"></script>
    <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-mapevents.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
    <script type="text/javascript" src='/assets/js/map.js?get=<?=time()?>'></script>
    <script type="text/javascript" src='/assets/js/script.js?get=<?=time()?>'></script>
</body>
</html>
