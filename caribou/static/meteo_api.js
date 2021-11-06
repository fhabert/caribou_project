const btnSubmit = document.getElementById('btn-submit');

btnSubmit.addEventListener('click', (event) => {
    const lat = document.getElementById('latitude-input').value;
    const long = document.getElementById('longitude-input').value;
    const api = `http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${apiKey}`;
    fetch(api)
        .then(response => response.json())
        .then((data) => {
            createCard(data);
        })
})

const createCard = (infos) => {
    const temp = Math.round(infos.main.temp - 273);
    const city = infos.name;
    const cardDiv = document.getElementById("card-weather");
    cardDiv.insertAdjacentHTML("beforeend", `<div class="card-white"><h3> ${city} <h3> \
        <ul class="list-element"> <li> <p>Description: ${infos.weather[0].description} </p></li> \
        <li> <p>Type: ${infos.weather[0].main} </p></li> <li> <p>Temp: ${temp}°C </p></li></ul></div>`);
    const ctx = document.getElementById('myChart').getContext('2d');
    const data = {
        labels: ["temp_min", "temp_max"],
        datasets: [{
            label: "Max Temp and min temp",
            data: [infos.main.temp_min, infos.main.temp_max],
        }],
        backgroundColor: [
            'rgba(153, 102, 255, 0.2)',
            'rgba(54, 162, 235, 0.2)'
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
        ],
        borderColor: '#777',
        borderWidth: 1,
    }
    let myChart = new Chart(ctx, {
        type: "bar",
        data: data,
        options: {
            scales: {
              y: {
                beginAtZero: true
              }
            },
            layout: {
                padding: {
                    left: 300,
                    right: 300, 
                    bottom:0,
                    top: 0
                }
            },
            maintainAspectRatio: false        
        }
    });
}