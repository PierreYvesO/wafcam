import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Cameras from './pages/Cameras';
import Home from "./pages/Home";
import NotFound from './pages/NotFound';

const App = () => {
  // test(){
  //   fetch('http://yourPCip:3000/users')
  //     .then(response => response.json())
  //     .then(users => console.warn(users))
  // }

  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/cameras" exact component={Cameras} />
        <Route component={NotFound} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
