import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from "./pages/Home";
import Cameras from './pages/Cameras';
import Rooms from './pages/Rooms';
import NotFound from './pages/NotFound';

const App = () => {
  const [rooms, setRooms] = useState([]);
  const [areas, setAreas] = useState([]);

  useEffect(() => {
    async function fetchData() {
      let response;
      response = await axios('http://localhost:4000/rooms');
      setRooms(response.data);
      response = await axios('http://localhost:4000/areas');
      setAreas(response.data);
    }
    fetchData();
  }, []);
  

  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/cameras" exact component={() => <Cameras areas={areas} />} />
        <Route path="/rooms" exact component={() => <Rooms rooms={rooms} />} />
        <Route component={NotFound} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
