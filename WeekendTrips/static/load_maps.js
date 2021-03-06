ymaps.ready(init_map());

function init_map() {
    navigator.geolocation.getCurrentPosition( function (position) {
        let longitude = position.coords.longitude;
        let latitude = position.coords.latitude;

        let geocode = longitude.toString() + ',' + latitude.toString()

        myMap = new ymaps.Map("map", {
            center: [latitude, longitude],
            zoom: 10
            }, {
                autoFitToViewport: 'always'
            });

        myPlacemark = new ymaps.Placemark([latitude, longitude], { content: 'Your current position!',
            balloonContent: 'Your current position' });

        myMap.geoObjects.add(myPlacemark);

        let api_key = "9a01f7c3-d337-4582-a99b-a765051710ed"
        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "https://geocode-maps.yandex.ru/1.x/?apikey=" + api_key + "&geocode=" + geocode
                + "&format=json&results=1&kind=locality",
            "method": "GET"
        }

        let response = $.ajax(settings).done(parseYandexResponse);
    })
}

function parseYandexResponse(data) {
    let city_name = data.response.GeoObjectCollection.featureMember[0].GeoObject.name
    console.log(city_name)
    document.getElementById('id_departure_city').value = city_name;
}

function error(err) {
    console.log(err)
}
