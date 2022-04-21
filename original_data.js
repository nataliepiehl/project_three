// Define local URL
var url = "http://127.0.0.1:5000/";

// Define query
var query = "api/ratings_load/";

// Define full query
var full_query = url + query;

//document.write(full_query);
console.log(full_query)

// Fetch the data
// fetch(full_query)
//     .then(response =>
//         response.json()
//     )
//     .then((data) => {
//         console.log(data)
//     })

// var ratings = data.ratings.title
//     console.log(ratings)


// init(data)

// let response = fetch(full_query);

// function init() {
    d3.json(full_query).then(data => {
        console.log(full_query);
        console.log(data);
        var names = data.ratings.title;
        let dropdownMenu = d3.select("#selDataset");
        // data.ratings.slice(0, 1000).forEach((name) => {
        data.ratings.forEach((name) => {
            dropdownMenu.append('option').text(name.title);
          })

          var result = names[0];

    buildMetadata(result)
    charts(result)
  });
// }

function optionChanged(value) {
  console.log(value);
  charts(value);
  buildMetadata(value);
}

// init();


// function buildRatings(movieTitle) {
//     d3.json("movie").then((data) => {
//         var movieName = data.0;
//         var resultArray = 0.filter(x => x.0 == movieTitle);
//         var result = resultArray[0];
//         console.log(result)
//         var PANEL = d3.select("movieTitle-0");
//         PANEL.html("");
//         Object.entries(result).forEach(([key, value]) => {
//             PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
//         })
//     })
// }