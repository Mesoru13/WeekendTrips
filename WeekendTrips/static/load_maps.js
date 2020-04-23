navigator.geolocation.getCurrentPosition(init, error)

function init(position){
    console.log(position)
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    let geocode = longitude.toString() + ',' + latitude.toString()

    let myMap = new ymaps.Map("map", {
        center: [latitude, longitude],
        zoom: 15
    });
    myMap.container.fitToViewport();
    ymaps.ready();

    let api_key = "9a01f7c3-d337-4582-a99b-a765051710ed"
    let settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://geocode-maps.yandex.ru/1.x/?apikey=" + api_key + "&geocode=" + geocode
            + "&format=json&results=1&kind=locality",
        "method": "GET"
    }

    let response = $.ajax(settings).done(parseYandexResponse);
}

function parseYandexResponse(data) {
    let city_name = data.response.GeoObjectCollection.featureMember[0].GeoObject.name
    console.log(city_name)
    document.getElementById('id_departure_city').value = city_name;
}

function error(err) {
    console.log(err)
}
