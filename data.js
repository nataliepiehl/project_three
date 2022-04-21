// Define local URL
var url = "http://127.0.0.1:5000/";

// Define query
var query = "api/ratings_load/";

// Define full query
var full_query = url + query;
console.log(full_query)

// Define bubble chart code
function bubblely_chart(x_value, y_value, bubble_size, hover_text){
// Passing in ratings_year, ratings_votes, ratings_rating, ratings_title as
// x_value, y_value, bubble_size, hover_text to create the bubble chart
console.log('bubble_size ', bubble_size);
// bubble_size = bubble_size * 1000   // Minimal change even with huge multipliers
console.log('bubble_size ', bubble_size);
var trace1 = {
    x: x_value,
    y: y_value,
    text: hover_text,
    mode: 'markers',
    marker: {
        color: x_value,
        size: bubble_size,  // Tried pop, and several other options
        // sizemode: 'area',
        // sizeref: 2.*max(size)/(40.**2),
        // sizemin: 4,
        hovermode: 'x unified',     // Tried x, y, y unified, closest
        colorscale: 'Jet'  // Closet color scale I could find at https://plotly.com/python/builtin-colorscales/
    }
  };

  var data = [trace1];

  var layout = {
    title: '',
    showlegend: false,
  };

  // Plot Buble Chart
  Plotly.newPlot('bubble', data, layout);
}

// function init() {
d3.json(full_query).then(data => {
    console.log(full_query);
    console.log(data);
    var names = data.ratings.title;
    let dropdownMenu = d3.select("#selDataset");
    data.ratings.slice(0, 1000).forEach((name) => {
        // data.ratings.forEach((name) => {
        dropdownMenu.append('option').text(name.title);
})

// Extract ratings data
ratings_id = data.ratings.map(d => d["id"]);
ratings_movie_id = data.ratings.map(d => d["movie_id"]);
ratings_rating = data.ratings.map(d => d["rating"]);
ratings_title = data.ratings.map(d => d["title"]);
ratings_votes = data.ratings.map(d => d["votes"]);
ratings_year = data.ratings.map(d => d["year"]);

// Execute bubble chart
bubblely_chart(ratings_year, ratings_votes, ratings_rating, ratings_title)

// Getting a reference to the input element on the page with the id property set to 'input-field'
var inputField = d3.select("#input-field");
console.log('inputField after call to bubblely_chart', inputField);

  // Input fields can trigger a change event when new text is entered.
  console.log('ratings_year ', ratings_year);
  inputField.on("change", function() {newText
      var newText = d3.event.target.value;
      console.log('The year selected is ', newText);

      input_output_panel(ratings_year, ratings_votes, ratings_rating, ratings_title, newText)

    });

});

function buildRatings(movieTitle) {
  d3.json(full_query).then((data) => {
      var movieName = data.ratings[0].title;
      var resultArray = data.ratings.filter(x => x.title == movieTitle)[0] || data.ratings[0];
      // var resultArray = movieName;
      console.log(movieName)
      // var result = resultArray;
      console.log(resultArray);
      var PANEL = d3.select("#sample-movieName");
      PANEL.html("");
      Object.entries(resultArray).forEach(([key, value]) => {
          PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
      })
  })
}

// Run initial ratings build
buildRatings("The Shawshank Redemption")

// Build outputs upon movie change
function optionChanged(value) {
    console.log(value);
    buildRatings(value);
    buildMetadata(value);
}

function input_output_panel(ratings_year, ratings_votes, ratings_rating, ratings_title, newText){
  // Passing in ratings_year, ratings_votes, ratings_rating, ratings_title, newText as 
  // ratings_year, ratings_votes, ratings_rating, ratings_title, newText
  for (var i = 0; i < ratings_year.length; i++) {
    var item = ratings_year[i];
    // console.log('Ratings_year[i] is ', ratings_year[i]);
    // console.log('item is ', item); 
    if (item == newText) { 
        var index = ratings_year.indexOf(item)
    }
  }
  console.log('A very popular movie in', newText, 'is'); 
  console.log('   Title:  ', ratings_title[index]);
  console.log('   Votes: ', ratings_votes[index]);
  console.log('   Rating: ', ratings_rating[index]);
  var md_a = []
  md_a['   Title     '] = ratings_title[index];
  md_a['   Votes  '] = ratings_votes[index];
  md_a['   Rating  '] = ratings_rating[index];
  var panel_metadata = d3.select("#sample-year");
  panel_metadata.html("");
  Object.entries(md_a).forEach(([key, value]) => {
    panel_metadata.append("h6").text(`${key}: ${value}`);
  });

}

var actor_query = url + "api/popular_people_load/";

// Pull actor data
d3.json(actor_query).then(data => {
    // Print query and data to console
    console.log(actor_query);
    console.log(data);

    // Populate dropdown menu
    let dropdownMenu = d3.select("#selActor");
    data.popular_people.forEach((person) => {
        dropdownMenu.append('option').text(person.name);
    })
});

// Generate timeline plot
function timelinePlot(person) {
    // Format person name for query
    var person_mod = person.replace(" ", "&");

    // Grab movies this person has been in
    var person_query = url + "api/person_load/" + person_mod;
    console.log(person_query)

    // Pull actor data
    d3.json(person_query).then(data => {
        // Print query and data to console
        console.log(data);

        // Define data lists
        var year = [];
        var votes = [];
        var rating = [];
        var title = []
        data.person_movies.forEach((movie) => {
            year.push(movie.year);
            votes.push(movie.votes);
            rating.push(movie.rating);
            title.push(movie.title);
        })

        // Format sizes
        rating_mod = rating.map(x => x * 5)

        // Define trace
        var trace = {
          x: year,
          y: votes,
          mode: 'markers',
          type: 'scatter',
          text: title,
          textposition: 'top',
          marker: {
              size: rating_mod,
              color: rating_mod,
            },
        };

        // Define data
        var data = [trace];

        // Define layout
        var layout = {
          title: person + ' Movies',
          xaxis: {
              showgrid: false,
              title: {
                    text: 'Year',
              },
          },
          yaxis: {
              showgrid: false,
              title: {
                      text: 'Number of Votes',
                },
          }
//          showlegend: true,
        };

        // Generate plot
        Plotly.newPlot('timeline', data, layout);
    });
}

// Generate initial timelinePlot
timelinePlot("John Belushi")

// When actor changes...
function actorChanged(person) {
  // Print change to console
  console.log(person);

  // Generate timeline plot
  timelinePlot(person)
}
