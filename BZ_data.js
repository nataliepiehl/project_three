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
        data.ratings.slice(0, 10).forEach((name) => {
        // data.ratings.forEach((name) => {
            dropdownMenu.append('option').text(name.title);
          })
          ratings_id = data.ratings.map(d => d["id"]);
          console.log('ratings_id ', ratings_id);
          ratings_movie_id = data.ratings.map(d => d["movie_id"]);
          console.log('ratings_movie_id  ', ratings_movie_id);
          ratings_rating = data.ratings.map(d => d["rating"]);
          console.log('ratings_rating ', ratings_rating);
          ratings_title = data.ratings.map(d => d["title"]);
          console.log('ratings_title  ', ratings_title);
          ratings_votes = data.ratings.map(d => d["votes"]);
          console.log('votes ', ratings_votes);
          ratings_year = data.ratings.map(d => d["year"]);
          console.log('ratings_year ', ratings_year);
          bubblely_chart(ratings_year, ratings_votes, ratings_rating, ratings_title)
      
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
function bubblely_chart(x_value, y_value, bubble_size, hover_text){
  // Passing in ratings_year, ratings_votes, ratings_rating, ratings_title as
  // x_value, y_value, bubble_size, hover_text to create the buble chart

  var trace1 = {
      x: x_value,
      y: y_value,
      text: hover_text,
      mode: 'markers',
      marker: {
          color: x_value,
          size: bubble_size
          // colorscale: 'Jet'  // Closet color scale I could find at https://plotly.com/python/builtin-colorscales/
      }
    };
    
    var data = [trace1];
    
    var layout = {
      title: '',
      showlegend: false,
      height: 600,
      width: 1200
    };
    // Plot Buble Chart
    Plotly.newPlot('bubble', data, layout);
}
