const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const cors = require('cors');
const http = require('http');

const connection = mysql.createPool({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : '2z2tz_patcam_test'
});

// Starting our app.
const app = express();
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cors());

// Creating a GET route that returns data from the 'room' table.
app.get('/rooms', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    // Executing the MySQL query (select all data from the 'room' table).
    connection.query('SELECT * FROM room', function (error, results, fields) {
      // When done with the connection, release it.
      connection.release();

      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.send(results);
    });
  });
});

// Creating a GET route that returns data from the 'entity' table.
app.get('/entities', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    // Executing the MySQL query (select all data from the 'entity' table).
    connection.query('SELECT * FROM entity', function (error, results, fields) {
      // When done with the connection, release it.
      connection.release();

      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.send(results);
    });
  });
});

// Creating a GET route that returns data from the 'forbidden_area' table.
app.get('/forbidden_areas', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    // Executing the MySQL query (select all data from the 'forbidden_area' table).
    connection.query('SELECT * FROM forbidden_area', function (error, results, fields) {
      // When done with the connection, release it.
      connection.release();

      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.send(results);
    });
  });
});

app.post('/forbidden_areas', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    const valuesToInsert = req.body.filter(area => typeof area.id === "string").map((area) => {
      delete area.id;
      return Object.values(area);
    });
    const valuesToUpdate = req.body.filter(area => area.id !== undefined).map((area) => {
      return Object.values(area);
    });
    console.log(valuesToUpdate);
    if (valuesToInsert.length > 0) {
      connection.query(
        'INSERT INTO forbidden_area (room_id, position_x, position_y, width, height) VALUES ?',
        [valuesToInsert],
        function (error, results, fields) {
          // If some error occurs, we throw an error.
          if (error) throw error;
        }
      );
    }
    if (valuesToUpdate.length > 0) {
      valuesToUpdate.map((area) => {
        connection.query(
          'UPDATE forbidden_area SET room_id = ?, position_x = ?, position_y = ?, width = ?, height = ? WHERE id = ?',
          area,
          function (error, results, fields) {
            // If some error occurs, we throw an error.
            if (error) throw error;
          }
        );
      })
    }
    // When done with the connection, release it.
    connection.release();
  });
});

// Starting our server.
app.listen(4000, () => {
  console.log('Go to http://localhost:4000/<route_name> so you can see the data.');
});
