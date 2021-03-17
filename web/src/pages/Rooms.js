import React from 'react';
import Navigation from '../components/Navigation';
import { DataGrid } from '@material-ui/data-grid';

const Rooms = (props) => {
  const { rooms } = props;

  const columns = [
    { field: 'id', headerName: 'ID', width: 100 },
    { field: 'name', headerName: 'Nom', width: 130 },
  ];

  return (
    <>
      <Navigation />
      <div className="Content">
        <h1>Pièces</h1>
        <div style={{ height: 400, width: '100%' }}>
          <DataGrid rows={rooms} columns={columns} pageSize={10} loading={rooms.length === 0} />
        </div>
      </div>
    </>
  );
}

export default Rooms;
