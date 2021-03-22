import React from 'react';
import Navigation from '../components/Navigation';
import CamTool from '../components/CamTool';
import { Button } from '@material-ui/core';
import { Edit, Save, AddBox, Delete } from '@material-ui/icons';
import axios from 'axios';

class Cameras extends React.Component {
  constructor(props) {
    super(props)
    this.camToolNode = React.createRef();
  }

  state = {
    imgHeight: 1,
    imgWidth: 1,
    imgNaturalHeight: 1,
    imgNaturalWidth: 1,
    editMode: false,
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
        room_id: 1,
        position_x: rect.x,
        position_y: rect.y,
        width: rect.width,
        height: rect.height
      }
    });
    axios.post('http://localhost:4000/forbidden_areas', areas)
  }

  render() {
    let cpt = 0;
    const initialRectangles = this.props.forbiddenAreas.map((area) => {
      cpt++;
      return {
        id: cpt,
        x: area.position_x * this.state.imgWidth / this.state.imgNaturalWidth,
        y: area.position_y * this.state.imgHeight / this.state.imgNaturalHeight,
        width: area.width * this.state.imgWidth / this.state.imgNaturalWidth,
        height: area.height * this.state.imgHeight / this.state.imgNaturalHeight,
        stroke: '#f00',
        strokeWidth: 4,
        draggable: this.state.editMode
      }
    });

    return (
      <>
        <Navigation />
        <div className="Content">
          <h1>Caméras</h1>
          <div className="camTool">
            <img src="./img/cam1.png" alt="caméra doguito" onLoad={this.handleImageLoaded.bind(this)} />
            <CamTool
              width={this.state.imgWidth}
              height={this.state.imgHeight}
              editMode={this.state.editMode}
              initialRectangles={initialRectangles}
              ref={this.camToolNode}
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
