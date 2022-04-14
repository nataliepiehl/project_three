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

