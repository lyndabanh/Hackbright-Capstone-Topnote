"use strict";

const data = {
  labels: [
    'Red',
    'Blue',
    'Yellow'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [300, 50, 100],
    backgroundColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)'
    ],
    hoverOffset: 4
  }]
};

// using jQuery
// const testChart2 = new Chart(
//   $('#test-chart2'),
//   {
//     type: 'pie',
//     data: data,
//   }
// );


// using vanilla js
const ctx2 = document.getElementById('test-chart2');
const testChart2 = new Chart(ctx2, {
    type: 'pie',
    data: data,
  }
);

const ctx = document.getElementById('test-chart');
const testChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['does', 'this', 'work'],
      datasets: [
        {data: [2, 4, 8]}
      ]
    }
  }
);