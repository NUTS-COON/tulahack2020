$(function() {
    $('#map').css('display', 'none');
    $('.search-input').focus(function (){
        $('.banner').css('display', 'none');
        $('#map').css('display', 'block');
    });
    $('.search-input').focusout(function (){
        var search = $('.search-input').val();
        $.ajax({
            url: '/data.html',
            method: 'post',
            data: {search: search},
            success: function(data){
                var json = JSON.parse(data);
                var group = new H.map.Group();
                map.removeObjects(map.getObjects());
                map.addObject(group);
                group.addEventListener('tap', function (evt) {
                    var bubble =  new H.ui.InfoBubble(evt.target.getGeometry(), {
                        content: evt.target.getData()
                    });
                    ui.addBubble(bubble);
                }, false);


                json.forEach(function(item, i, arr) {
                    addMarkerToGroup(group, {lat:item.lat, lng:item.lon},
                        '<div class="window"><h3>' + item.name +'</h3><p>Цена: ' + item.price + '</p><p>Адрес: ' + item.address +'</p></div>');
                });

            },
        });
    });
});