import { MenuItem, MenuList, Paper } from '@material-ui/core';
import { Videocam, Home, Toc } from '@material-ui/icons';
import React from 'react';
import { NavLink } from 'react-router-dom';

const Navigation = () => {
  return (
    <Paper className={"Navigation"}>
      <MenuList>
        <NavLink exact to="/">
          <MenuItem>
            <Home />
            Accueil
          </MenuItem>
        </NavLink>
        <NavLink exact to="cameras">
          <MenuItem>
            <Videocam />
            Caméras
          </MenuItem>
        </NavLink>
        <NavLink exact to="rooms">
          <MenuItem>
            <Toc />
            Pièces
          </MenuItem>
        </NavLink>
      </MenuList>
    </Paper>
  );
}
  
export default Navigation;