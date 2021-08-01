"use strict";

$.get('/fav_countries.json', (res) => {
  const data = [];
  for (const item of res.data) {
    data.push({x: item.country, y: item.num_fav});
  }
  const labels = [];
  for (const country of res.data) {
    labels.push(country.country);
  }

   new Chart(
    $('#line-chart'),
    {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
            label: 'Countries',
            data: data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
          }
        ]
      }
    }
  );
});


$.get('/fav_countries.json', (res) => {
  // const labels = [];
  // for (const country of res.data) {
  //   labels.push(country.country);
  // }
  const labels = [];
  const datas = [];
  const colors = [];
  for (const item of res.data) {
    labels.push(item.country);
    datas.push(item.num_fav);
    colors.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
  }

// look up how to randomly select colors
// console.log(datas,labels)
  new Chart(
    $('#pie-chart'),
    {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Countries of Favorite Wines',
          data: datas,
          backgroundColor: colors,
          // backgroundColor: [
          //   'rgb(255, 99, 132)',
          //   'rgb(54, 162, 235)',
          //   'rgb(255, 205, 86)'
          //   ],
        }]
      }
    }
  );
});

$.get('/fav_countires.json', (res) => {
  // const labels = [];
  // for (const country of res.data) {
  //   labels.push(country.country);
  // }
  const labels = [];
  const datas = [];
  const colors = [];
  for (const item of res.data) {
    labels.push(item.country);
    datas.push(item.num_fav);
    colors.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
  }


console.log(datas,labels)
  new Chart(
    $('#bar-chart'),
    {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Most Favorited Countries',
          data: datas,
          backgroundColor: colors,
          borderColor: colors,
          borderWidth: 1,
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          }
        }
      }
    }
  );
});

  
$.get('/fav_varietals.json', (res) => {
  // const labels = [];
  // for (const country of res.data) {
  //   labels.push(country.country);
  // }
  const labels2 = [];
  const data2 = [];
  const colors2 = [];
  for (const item of res.data) {
    labels2.push(item.variety);
    data2.push(item.num_fav);
    colors2.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
  }

console.log(data2,labels2,colors2),
  new Chart(
    $('#pie-chart2'),
    {
      type: 'pie',
      data: {
        labels: labels2,
        datasets: [{
          label: 'Favorite Wine Varietals',
          data: data2,
          backgroundColor: colors2,
        }]
      }
    }
  );
});