import React from 'react';
import Navigation from '../components/Navigation';
import CamTool from '../components/CamTool';
import { Button } from '@material-ui/core';
import { Edit, Save, AddBox, Delete } from '@material-ui/icons';

class Cameras extends React.Component {
  constructor(props) {
    super(props)
    this.camToolNode = React.createRef();
  }

  state = {
    imgHeight: 0,
    imgWidth: 0,
    editMode: false,
  };

  handleImageLoaded() {
    const img = document.querySelector("div>img");
    this.setState({
      imgHeight: img.height,
      imgWidth: img.width
    })
  }

  render() {
    const initialRectangles = [
      {
        x: 50,
        y: 50,
        width: 100,
        height: 100,
        stroke: '#f00',
        strokeWidth: 4,
        id: 1,
        draggable: this.state.editMode
      }
    ];

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
                  })
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
