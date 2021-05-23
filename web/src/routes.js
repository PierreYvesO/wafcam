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

// Creating a GET route that returns data from the 'forbidden_area' table.
app.get('/areas', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    // Executing the MySQL query (select all data from the 'forbidden_area' table).
    connection.query('SELECT * FROM area', function (error, results, fields) {
      // When done with the connection, release it.
      connection.release();

      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.send(results);
    });
  });
});

// Creating a POST route that insert or update area(s) in the 'area' table.
app.post('/areas', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    const valuesToInsert = req.body.filter(area => typeof area.id_area === "string").map((area) => {
      delete area.id_area;
      return Object.values(area);
    });
    const valuesToUpdate = req.body.filter(area => area.id_area !== undefined).map((area) => {
      return Object.values(area);
    });
    if (valuesToInsert.length > 0) {
      connection.query(
        'INSERT INTO area (id_camera, name, x, y, w, h) VALUES ?',
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
          'UPDATE area SET id_camera = ?, name = ?, x = ?, y = ?, w = ?, h = ? WHERE id_area = ?',
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

// Creating a DELETE route that delete one area by id from the 'area' table.
app.delete('/area/:id', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    connection.query(
      'DELETE FROM area WHERE id_area = ?',
      req.params.id,
      function (error, results, fields) {
        // If some error occurs, we throw an error.
        if (error) throw error;
      }
    );
    connection.release();
  });
});

// Creating a GET route that returns data from the 'camera' table.
app.get('/cameras', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    // Executing the MySQL query (select all data from the 'room' table).
    connection.query('SELECT * FROM camera', function (error, results, fields) {
      // If some error occurs, we throw an error.
      if (error) throw error;

      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      res.send(results);

      // When done with the connection, release it.
      connection.release();
    });
  });
});

// Creating a DELETE route that delete one room by id from the 'room' table and all cameras from the 'camera' table link to this room.
app.delete('/room/:id', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    connection.query(
      'DELETE FROM camera WHERE id_room = ?;',
      req.params.id,
      function (error, results, fields) {
        // If some error occurs, we throw an error.
        if (error) throw error;
      }
    );
    connection.query(
      'DELETE FROM room WHERE id_room = ?',
      req.params.id,
      function (error, results, fields) {
        // If some error occurs, we throw an error.
        if (error) throw error;
      }
    );
    connection.release();
  });
});

// Creating a PUT route that insert or update a room in the 'room' table.
app.put('/room', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    if (req.body.id_room === null) {
      connection.query(
        'INSERT INTO room (name) VALUES (?)',
        [req.body.name],
        function (error, results, fields) {
          // If some error occurs, we throw an error.
          if (error) throw error;
        }
      );
    } else {
      connection.query(
        'UPDATE room SET name = ? WHERE id_room = ?',
        [req.body.name, req.body.id_room],
        function (error, results, fields) {
          // If some error occurs, we throw an error.
          if (error) throw error;
        }
      );
    }
    // When done with the connection, release it.
    connection.release();
  });
});

// Creating a DELETE route that delete one camera from the 'camera' table.
app.delete('/camera/:id', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    connection.query(
      'DELETE FROM camera WHERE id_camera = ?;',
      req.params.id,
      function (error, results, fields) {
        // If some error occurs, we throw an error.
        if (error) throw error;
      }
    );
    connection.release();
  });
});

// Creating a PUT route that insert or update a camera in the 'camera' table.
app.put('/camera', function (req, res) {
  // Connecting to the database.
  connection.getConnection(function (err, connection) {
    
    console.log(bcrypt.hash('test', 10));
    if (req.body.id_camera === null) {
      connection.query(
        'INSERT INTO camera (ip_adress, user, password, id_room) VALUES (?)',
        [[req.body.ip_adress, req.body.user, req.body.password, req.body.id_room]],
        function (error, results, fields) {
          // If some error occurs, we throw an error.
          if (error) throw error;
        }
      );
    } else {
      connection.query(
        'UPDATE camera SET ip_adress = ?, user = ?, password = ?, id_room = ? WHERE id_camera = ?',
        [req.body.ip_adress, req.body.user, req.body.password, req.body.id_room, req.body.id_camera],
        function (error, results, fields) {
          // If some error occurs, we throw an error.
          if (error) throw error;
        }
      );
    }
    // When done with the connection, release it.
    connection.release();
  });
});

// Starting our server.
app.listen(4000, () => {
  console.log('Go to http://localhost:4000/<route_name> so you can see the data.');
});
