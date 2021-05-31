import React from 'react';
import Navigation from '../components/Navigation';
import CamTool from '../components/CamTool';
import { Button, Paper, Tab, Tabs } from '@material-ui/core';
import { Edit, Save, AddBox, Delete } from '@material-ui/icons';
import axios from 'axios';

class Cameras extends React.Component {
  constructor(props) {
    super(props)
    this.camToolNode = React.createRef();
  }

  state = {
    cameras: this.props.cameras,
    imgHeight: 1,
    imgWidth: 1,
    imgNaturalHeight: 1,
    imgNaturalWidth: 1,
    editMode: false,
    tabValue: 0
  };

  handleImageLoaded() {
    const img = document.querySelector("div>img");
    this.setState({
      imgHeight: img.height,
      imgWidth: img.width,
      imgNaturalHeight: img.naturalHeight,
      imgNaturalWidth: img.naturalWidth,
    });
  }

  handleSave() {
    const areas = this.camToolNode.current.state.rectangles.map((rect) => {
      return {
        id_camera: this.props.cameras[this.state.tabValue].id_camera,
        name: rect.name,
        x: Math.round(rect.x * this.state.imgNaturalWidth / this.state.imgWidth),
        y: Math.round(rect.y * this.state.imgNaturalHeight / this.state.imgHeight),
        w: Math.round(rect.width * this.state.imgNaturalWidth / this.state.imgWidth),
        h: Math.round(rect.height * this.state.imgNaturalHeight / this.state.imgHeight),
        id_area: rect.id
      }
    });
    axios.post('http://localhost:4000/areas', areas);
    window.location.reload();
  }

  handleChangeTab(event, newValue) {
    this.setState({
      tabValue: newValue
    });
  }

  render() {
    var initialRectangles = [{}];
    var url = "";
    var idCamProps = null;
    if (this.state.cameras.length !== 0) {
      if (this.state.imgHeight !== 1) {
        initialRectangles = this.props.areas.filter(area => area.id_camera === this.state.cameras[this.state.tabValue].id_camera).map((area) => {
          return {
            id: area.id_area,
            x: area.x * this.state.imgWidth / this.state.imgNaturalWidth,
            y: area.y * this.state.imgHeight / this.state.imgNaturalHeight,
            width: area.w * this.state.imgWidth / this.state.imgNaturalWidth,
            height: area.h * this.state.imgHeight / this.state.imgNaturalHeight,
            stroke: '#f00',
            strokeWidth: 4,
            draggable: this.state.editMode,
            name: area.name
          }
        });
        idCamProps = this.state.cameras[this.state.tabValue].id_camera;
      }
      url = "http://" + this.state.cameras[this.state.tabValue].ip_adress + "/videostream.cgi?user=" + this.state.cameras[0].user + "&pwd=" + this.state.cameras[0].password;
    } else {
      url = "./img/unknown_camera.jpg";
    }

    return (
      <>
        <Navigation />
        <div className="Content">
          <h1>Caméras</h1>
          {this.state.cameras.length !== 0 && (
            <Paper>
              <Tabs
                value={this.state.tabValue}
                onChange={this.handleChangeTab.bind(this)}
                indicatorColor="primary"
                textColor="primary"
              >
                {this.state.cameras.map((camera) => (
                  <Tab key={camera.id_camera} label={this.props.rooms.filter(room => room.id_room === camera.id_room)[0].name + ' (' + camera.ip_adress + ')'} disabled={this.state.editMode} />
                ))}
              </Tabs>
            </Paper>
          )}
          <div className="camTool">
            <img src={url} alt="webcam" onLoad={this.handleImageLoaded.bind(this)} />
            <CamTool
              width={this.state.imgWidth}
              height={this.state.imgHeight}
              editMode={this.state.editMode}
              initialRectangles={initialRectangles}
              ref={this.camToolNode}
              id_camera={idCamProps}
            />
            <div className="buttons">
              <div>
                {this.state.editMode && (
                  <>
                    <Button
                      variant={"contained"}
                      color={"inherit"}
                      onClick={() => {
                        this.camToolNode.current.addRectangle()
                      }}
                      startIcon={<AddBox />}
                      size={"large"}
                    >
                      Ajouter une zone
                    </Button>
                    <Button
                      variant={"contained"}
                      color={"secondary"}
                      onClick={() => {
                        this.camToolNode.current.deleteRectangle()
                      }}
                      startIcon={<Delete />}
                      size={"large"}
                    >
                      Supprimer une zone
                    </Button>
                  </>
                )}
              </div>
              <Button
                variant={"contained"}
                color={this.state.editMode ? "primary" : "default"}
                onClick={() => {
                  this.setState({
                    editMode: !this.state.editMode
                  });
                  this.state.editMode && this.handleSave();
                }}
                startIcon={this.state.editMode ? <Save /> : <Edit />}
                size={"large"}
                disabled={this.state.cameras.length === 0}
              >
                {this.state.editMode ? "Enregistrer" : "Éditer"}
              </Button>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Cameras;
