const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const connection = mysql.createPool({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : '2z2tz_patcam_test'
});

// Starting our app.
const app = express();

// Creating a GET route that returns data from the 'users' table.
app.get('/rooms', function (req, res) {
    // Connecting to the database.
    connection.getConnection(function (err, connection) {

    // Executing the MySQL query (select all data from the 'users' table).
    connection.query('SELECT * FROM room', function (error, results, fields) {
      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000')
      res.send(results)
    });
  });
});

// Creating a GET route that returns data from the 'users' table.
app.get('/entities', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {

  // Executing the MySQL query (select all data from the 'users' table).
  connection.query('SELECT * FROM entity', function (error, results, fields) {
    // If some error occurs, we throw an error.
    if (error) throw error;

    // Getting the 'response' from the database and sending it to our route. This is were the data is.
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000')
    res.send(results)
  });
});
});

// Starting our server.
app.listen(4000, () => {
  console.log('Go to http://localhost:4000/<route_name> so you can see the data.');
});