if ('geolocation' in navigator) {
   console.log('geolocation available');
   navigator.geolocation.getCurrentPosition(async function(position) {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      // console.log(lat)
      // console.log(lon)

      // document.getElementById('latitude').textContent = lat;
      // document.getElementById('longitude').textContent = lon;
      
      const data = {'lat': lat, 'lon': lon};
      const options = {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify(data)
      };
      
      // send location to server
      const response = await fetch('/weather_data', options);

      // get data from server
      const weather = await response.json();
      // console.log(weather);

      // unpack data
      const temp = weather['temp']
      const pressure = weather['pressure']
      const humidity = weather['humidity']
      const min_temp = weather['temp_min']
      const max_temp = weather['temp_max']
      const ozone = weather['parameter']
      const ozone_level = weather['value']
      const unit = weather['unit']
      const air_update = weather['lastUpdated']
      
      // output weather data to html
      // for (var key in weather) {
      //    // console.log(key);
      //    const root = document.createElement('div');
      //    const geo = document.createElement('div');

      //    geo.textContent = key + ': ' + weather[key];
         
      //    root.append(geo);
      //    document.body.append(root);
      // }

      const txt = `The weather at ${lat}&deg;, ${lon}&deg; is ${temp}&deg; F with a
      humidity level of ${humidity}% and an air pressure level of ${pressure} atm.
      The maximum temperature today is ${max_temp}&deg; F and the low so far is
      ${min_temp}&deg; F. The ${ozone} level is ${ozone_level} ${unit} and was 
      last updated ${air_update}.`;


      // set up map
      const mymap = L.map('map').setView([lat, lon], 15);
      const attribution = 
         '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

      const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      const tiles = L.tileLayer(tileUrl, {attribution});
      tiles.addTo(mymap);
      const marker = L.marker([lat, lon]).addTo(mymap);
      marker.bindPopup(txt);
   });
}

else {
   console.log('geolocation not available');
}