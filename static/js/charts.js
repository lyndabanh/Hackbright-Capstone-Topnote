"use strict";

// LINE CHART - FAV COUNTRIES (TESTING)
// $.get('/fav_countries.json', (res) => {
//   const data = [];
//   for (const item of res.data) {
//     data.push({x: item.country, y: item.num_fav});
//   }
//   const labels = [];ß
//   for (const country of res.data) {
//     labels.push(country.country);
//   }

//    new Chart(
//     $('#line-chart'),
//     {
//       type: 'line',
//       data: {
//         labels: labels,
//         datasets: [{
//             label: 'Countries',
//             data: data,
//             fill: false,
//             borderColor: 'rgb(75, 192, 192)',
//           }
//         ]
//       }
//     }
//   );
// });

// PIE CHART - FAV COUNTRIES
$.get('/fav_countries.json', (res) => {
  const labels2 = [];
  const data2 = [];
  const colors2 = [];
  for (const item of res.data) {
    labels2.push(item.country);
    data2.push(item.num_fav);
    colors2.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
  }

// look up how to randomly select colors
// console.log(datas,labels)
  new Chart(
    $('#pie-chart'),
    {
      type: 'pie',
      data: {
        labels: labels2,
        datasets: [{
          label: 'Countries of Favorite Wines',
          data: data2,
          backgroundColor: colors2,
        }]
      }
    }
  );
});

// BAR CHART - FAV COUNTRIES
// $.get('/fav_countires.json', (res) => {
//   const labels3 = [];
//   const data3 = [];
//   const colors3 = [];
//   for (const item of res.data) {
//     labels3.push(item.country);
//     data3.push(item.num_fav);
//     colors3.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
//   }

//   new Chart(
//     $('#bar-chart'),
//     {
//       type: 'bar',
//       data: {
//         labels: labels3,
//         datasets: [{
//           label: 'Most Favorited Countries',
//           data: data3,
//           backgroundColor: colors3,
//           borderColor: colors3,
//           borderWidth: 1,
//         }]
//       },
//       // options: {
//       //   scales: {
//       //     y: {
//       //       beginAtZero: true,
//       //     }
//       //   }
//       // }
//     }
//   );
// });

// PIE CHART - FAV VARIETALS
$.get('/fav_varietals.json', (res) => {
  const labels4 = [];
  const data4 = [];
  const colors4 = [];
  for (const item of res.data) {
    labels4.push(item.variety);
    data4.push(item.num_fav);
    colors4.push(`rgb(${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)},${Math.floor(Math.random() * 255)})`)
  }

console.log(data4,labels4,colors4),
  new Chart(
    $('#pie-chart2'),
    {
      type: 'pie',
      data: {
        labels: labels4,
        datasets: [{
          label: 'Favorite Wine Varietals',
          data: data4,
          backgroundColor: colors4,
        }]
      }
    }
  );
});

// LINE CHART - USER VS CRITIC RATING
$.get('/ratings.json', (res) => {
  const data3 = [];
  for (const item of res.data) {
    data3.push({x: item.wine_id, y: item.user_rating});
  }
  const data3b = [];
  for (const item of res.data) {
    data3b.push({x: item.wine_id, y: item.critic_rating});
  }
  const labels3 = [];
  for (const item of res.data) {
    labels3.push(item.wine_id);
  }

  new Chart(
    $('#line-chart2'),
    {
      type: 'line',
      data: {
        labels: labels3,
        datasets: [{
          label: 'User Rating',
          data: data3,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'Critic Rating',
          data: data3b,
          fill: false,
          borderColor: 'rgb(153, 76, 0)',
          tension: 0.1
        }]
      }
    }
  );
});

// SCATTER CHART
$.get('/ratings.json', (res) => {
  const data3 = [];
  for (const item of res.data) {
    data3.push({x: item.user_rating, y: item.critic_rating});
  }
  const data3b = [];
  for (const item of res.data) {
    data3b.push({x: item.wine_id, y: item.critic_rating});
  }
  const labels3 = [];
  for (const item of res.data) {
    labels3.push(item.wine_id);
  }

  new Chart(
    $('#scatter-chart'),
    {
      type: 'scatter',
      data: {
        labels: labels3,
        datasets: [
          {
            label: 'User vs Critic rating',
            data: data3,
            borderColor: 'rgb(75, 192, 192)',
            bacgroundColor: 'rgb(75, 192, 192)',
          },
          // {
          //   label: 'Critic Rating',
          //   data: data3b,
          //   borderColor: 'rgb(233, 192, 192)',
          //   bacgroundColor: 'rgb(233, 192, 192)',
          // }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Chart.js Scatter Chart'
          }
        }
      },
    }
  );
});