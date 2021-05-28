import React, { useState } from 'react';
import Navigation from '../components/Navigation';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  FormControl,
  IconButton,
  InputLabel,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
  ListSubheader,
  OutlinedInput,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@material-ui/core';
import { Edit, Delete, Save, Add } from '@material-ui/icons';
import axios from 'axios';

const Rooms = (props) => {
  const { rooms, cameras } = props;
  const [displayDialogDeleteRoom, setDisplayDialogDeleteRoom] = useState(false);
  const [roomToDelete, setRoomToDelete] = useState({
    id_room: null,
    name: ''
  });
  const [roomToUpsert, setRoomToUpsert] = useState({
    id_room: null,
    name: ''
  });
  const [cameraToUpsert, setCameraToUpsert] = useState({
    id_camera: null,
    ip_adress: '',
    user: '',
    password: '',
    id_room: null
  });
  const columns = [
    { i: 0, name: 'Nom' },
    { i: 1, name: 'Nombre de caméra' },
    { i: 2, name: '' }
  ];

  const rows = rooms.map((room) => {
    const camera_count = cameras.filter(camera => camera.id_room === room.id_room).length;
    return {
      ...room,
      camera_count: camera_count
    }
  });

  function handleResetRoomForm() {
    setRoomToUpsert({
      id_room: null,
      name: ''
    });
  }

  function handleResetCamForm() {
    setCameraToUpsert({
      id_camera: null,
      ip_adress: '',
      user: '',
      password: '',
      id_room: null
    });
  }

  function handleDeleteRoom() {
    axios.delete('http://localhost:4000/room/' + roomToDelete.id_room);
    handleResetRoomForm();
    window.location.reload();
  }

  function handleSaveRoom() {
    axios.put('http://localhost:4000/room', roomToUpsert);
    handleResetRoomForm();
    window.location.reload();
  }

  function handleDeleteCamera(id_camera) {
    axios.delete('http://localhost:4000/camera/' + id_camera);
    window.location.reload();
  }

  function handleSaveCamera() {
    axios.put('http://localhost:4000/camera', cameraToUpsert);
    handleResetCamForm();
    window.location.reload();
  }

  return (
    <>
      <Navigation />
      <div className="Content">
        <h1>Pièces</h1>
        <div className="roomTool">
          <TableContainer component={Paper} className={'roomTable'}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  {columns.map((column) => (
                    <TableCell key={column.i} align="center">{column.name}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow key={row.id_room}>
                    <TableCell align="center">{row.name}</TableCell>
                    <TableCell align="center">{row.camera_count}</TableCell>
                    <TableCell align="center">
                      <IconButton
                        color="primary"
                        onClick={() => {
                          setRoomToUpsert({
                            id_room: row.id_room,
                            name: row.name
                          })
                        }}  
                        title="Modifier la pièce"
                      >
                        <Edit />
                      </IconButton>
                      &emsp;
                      <IconButton
                        color="secondary"
                        onClick={() => {
                          setRoomToDelete({
                            id_room: row.id_room,
                            name: row.name
                          })
                          setDisplayDialogDeleteRoom(true);
                        }}
                        title="Supprimer la pièce"
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <Button
              variant={"contained"}
              color={"inherit"}
              onClick={handleResetRoomForm}
              startIcon={<Add />}
            >
              Ajouter une pièce
            </Button>
          </TableContainer>
          <Paper className={'roomForm'}>
            <h3>Ajouter / Modifier une pièce</h3>
            <br/>
              <FormControl variant="outlined">
                <InputLabel htmlFor="roomName">Nom</InputLabel>
                <OutlinedInput
                  id="roomName"
                  value={roomToUpsert.name}
                  label="Nom"
                  onChange={(e) =>{
                    setRoomToUpsert({
                      ...roomToUpsert,
                      name: e.target.value
                    })
                  }}
                  autoFocus={roomToUpsert.name !== ''}
                />
              </FormControl>
              <List className={'camList'} subheader={
                <ListSubheader>
                  Caméras
                  <IconButton
                    className="addCamButton"
                    title="Ajouter une caméra"
                    onClick={() => {
                      if (roomToUpsert.id_room !== null) {
                        setCameraToUpsert({
                          ...cameraToUpsert,
                          id_room: roomToUpsert.id_room
                        });
                      } else {
                        alert('Veuillez d\'abord enregistrer votre nouvelle pièce avec un nom avant d\'y ajouter une caméra');
                      }
                    }}
                  >
                    <Add />
                  </IconButton>
                </ListSubheader>
              }>
                {cameras.filter(camera => camera.id_room === roomToUpsert.id_room).map((cam) => (
                  <ListItem button key={cam.id_camera}>
                    <ListItemText primary={cam.ip_adress} />
                    <ListItemSecondaryAction>
                      <IconButton
                        size="small"
                        title="Modifier la caméra"
                        onClick={() => {
                          setCameraToUpsert({
                            id_camera: cam.id_camera,
                            ip_adress: cam.ip_adress,
                            user: cam.user,
                            password: cam.password,
                            id_room: cam.id_room
                          });
                        }}
                      >
                        <Edit />
                      </IconButton>
                      &emsp;
                      <IconButton
                        size="small"
                        title="Supprimer la caméra"
                        onClick={() => handleDeleteCamera(cam.id_camera)}
                      >
                        <Delete />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
                {(cameras.filter(camera => camera.id_room === roomToUpsert.id_room).length === 0) && (
                  <ListItem>Aucune caméra enregistrée...</ListItem>
                )}
              </List>
              <Button
                variant={"contained"}
                color={"primary"}
                startIcon={<Save />}
                onClick={handleSaveRoom}
              >
                Enregistrer
              </Button>
          </Paper>
        </div>
      </div>
      <Dialog
        open={displayDialogDeleteRoom}
        onClose={() => setDisplayDialogDeleteRoom(false)}
      >
        <DialogTitle>Voulez-vous vraiment supprimer la pièce "{roomToDelete.name}" ?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Cela entraînera la suppression de toutes les caméras enregistrées et liées à cette pièces ainsi que toutes les zones interdites définies sur ces caméras.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              handleDeleteRoom();
              setDisplayDialogDeleteRoom(false);
            }}
            color="primary"
            autoFocus
          >
            Oui
          </Button>
          <Button
            onClick={() => {
              setDisplayDialogDeleteRoom(false);
            }}
            color="secondary"
          >
            Non
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog
        open={cameraToUpsert.id_room !== null}
        onClose={handleResetCamForm}
      >
        <DialogTitle>Ajouter / Modifier une caméra</DialogTitle>
        <DialogContent>
          <FormControl variant="outlined">
            <InputLabel htmlFor="camIp">Adresse IP</InputLabel>
            <OutlinedInput
              id="camIp"
              value={cameraToUpsert.ip_adress}
              label="Adresse IP"
              onChange={(e) =>{
                setCameraToUpsert({
                  ...cameraToUpsert,
                  ip_adress: e.target.value
                })
              }}
              autoFocus={cameraToUpsert.ip_adress !== ''}
            />
          </FormControl>
          <br/>
          <FormControl variant="outlined">
            <InputLabel htmlFor="camUser">Nom d'utilisateur</InputLabel>
            <OutlinedInput
              id="camUser"
              value={cameraToUpsert.user}
              label="Nom d'utilisateur"
              onChange={(e) =>{
                setCameraToUpsert({
                  ...cameraToUpsert,
                  user: e.target.value
                })
              }}
            />
          </FormControl>
          <br/>
          <FormControl variant="outlined">
            <InputLabel htmlFor="camPass">Mot de passe</InputLabel>
            <OutlinedInput
              id="camPass"
              value={cameraToUpsert.password}
              label="Mot de passe"
              type={'password'}
              onChange={(e) =>{
                setCameraToUpsert({
                  ...cameraToUpsert,
                  password: e.target.value
                })
              }}
            />
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button
            variant={"contained"}
            color={"primary"}
            startIcon={<Save />}
            onClick={handleSaveCamera}
          >
            Enregistrer
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default Rooms;
