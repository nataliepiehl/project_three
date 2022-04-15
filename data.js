// Define local URL
var url = "http://127.0.0.1:5000/";

// Define query
var query = "api/movies_load/";

// Define title of interest
//var title = "the&mummy";

// Define year of interest
// var year = 1955

// Define full query
console.log(url)
console.log(query)
let full_query = url + query;

//document.write(full_query);
console.log(full_query)

// Fetch the data
fetch(full_query)
    .then(response =>
        response.json()
    )
    .then((data) => {
        console.log(data)
    })

// let response = fetch(full_query);

// function buildMovie(movieTitle) {
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