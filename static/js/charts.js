"use strict";

// const data = {
//   labels: [
//     'Red',
//     'Blue',
//     'Yellow'
//   ],
//   datasets: [{
//     label: 'My First Dataset',
//     data: [300, 50, 100],
//     backgroundColor: [
//       'rgb(255, 99, 132)',
//       'rgb(54, 162, 235)',
//       'rgb(255, 205, 86)'
//     ],
//     hoverOffset: 4
//   }]
// };

// // using jQuery
// // const testChart2 = new Chart(
// //   $('#test-chart2'),
// //   {
// //     type: 'pie',
// //     data: data,
// //   }
// // );


// // using vanilla js
// const ctx2 = document.getElementById('test-chart2');
// const testChart2 = new Chart(ctx2, {
//     type: 'pie',
//     data: data,
//   }
// );

// const ctx = document.getElementById('test-chart');
// const testChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: ['does', 'this', 'work'],
//       datasets: [
//         {data: [2, 4, 8]}
//       ]
//     }
//   }
// );


// $.get('/sales_this_week.json', (res) => {
//   // We need to restructure the generic data we got from the server. In this
//   // case, we need an array of objects like this:
//   // [{x: xValue, y: yValue}, ...,]
//   const data = [];
//   for (const dailyTotal of res.data) {
//     data.push({x: dailyTotal.date, y: dailyTotal.melons_sold});
//   }

//   // Since Chart.js doesn't understand that we want to plot this data by *time*,
//   // the resulting line graph is really ugly.
//   //
//   // See the next demo for how to use times on the x- or y-axis.
//   new Chart(
//     $('#line-chart'),
//     {
//       type: 'line',
//       data: {
//         datasets: [
//           {
//             label: 'All Melons',
//             data: data
//           }
//         ]
//       }
//     }
//   );
// });

$.get('/test.json', (res) => {
  const data = [];
  for (const item of res.data) {
    data.push({x: item.favorite_id, y : item.user_id});
  }

  new Chart(
    $('#line-chart'),
    {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Test',
            data: data
          }
        ]
      }
    }
  );
});