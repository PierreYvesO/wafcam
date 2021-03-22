import React from 'react';
import { Stage, Rect, Layer, Transformer } from 'react-konva';

const Rectangle = ({ shapeProps, isSelected, onSelect, onChange, canvasSize, editMode }) => {
  const shapeRef = React.useRef();
  const trRef = React.useRef();

  React.useEffect(() => {
    if (isSelected && editMode) {
      // we need to attach transformer manually
      trRef.current.nodes([shapeRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [isSelected, editMode]);

  return (
    <React.Fragment>
      <Rect
        onClick={onSelect}
        onTap={onSelect}
        ref={shapeRef}
        {...shapeProps}
        draggable={editMode}
        stroke={editMode ? '#0f0' : '#f00'}
        onDragEnd={(e) => {
          onChange({
            ...shapeProps,
            x: e.target.x(),
            y: e.target.y(),
          });
        }}
        dragBoundFunc={(pos) => {
          let newX = pos.x;
          let newY = pos.y;
          if (pos.x < 0) {
            newX = 1;
          } else if (pos.x + shapeProps.width > canvasSize.width) {
            newX = canvasSize.width - shapeProps.width - 1;
          }
          if (pos.y < 0) {
            newY = 1;
          } else if (pos.y + shapeProps.height > canvasSize.height) {
            newY = canvasSize.height - shapeProps.height - 1;
          }
          return {
            x: newX,
            y: newY,
          }
        }}
        onTransformEnd={(e) => {
          // transformer is changing scale of the node
          // and NOT its width or height
          // but in the store we have only width and height
          // to match the data better we will reset scale on transform end
          const node = shapeRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          // we will reset it back
          node.scaleX(1);
          node.scaleY(1);
          onChange({
            ...shapeProps,
            x: node.x(),
            y: node.y(),
            // set minimal value
            width: Math.max(5, node.width() * scaleX),
            height: Math.max(node.height() * scaleY),
          });
        }}
      />
      {isSelected && editMode && (
        <Transformer
          ref={trRef}
          borderStroke={'green'}
          rotateEnabled={false}
          boundBoxFunc={(oldBox, newBox) => {
            // limit resize
            if (newBox.width < 50
              || newBox.height < 50
              || newBox.x < -1
              || newBox.y < -1
              || newBox.x + newBox.width > canvasSize.width + 1
              || newBox.y + newBox.height > canvasSize.height + 1) {
              return oldBox;
            }
            return newBox;
          }}
        />
      )}
    </React.Fragment>
  );
};

class CamTool extends React.Component {
  state = {
    rectangles: this.props.initialRectangles,
    selectedId: null,
    countRectangles: 1
  };

  checkDeselect = (e) => {
    // deselect when clicked on empty area
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      this.setState({
        selectedId: null
      });
    }
  };
  
  addRectangle = () => {
    this.state.rectangles.push({
      x: 50,
      y: 50,
      width: 100,
      height: 100,
      stroke: '#f00',
      strokeWidth: 4,
      id: this.state.countRectangles + 1,
      draggable: this.props.editMode
    });
    this.setState({
      countRectangles: this.state.countRectangles + 1,
      selectedId: this.state.countRectangles + 1
    });
    this.forceUpdate();
  };

  deleteRectangle = () => {
    for (let i = 0; i < this.state.rectangles.length; i++) {
      if (this.state.rectangles[i].id === this.state.selectedId) {
        this.state.rectangles.splice(i, 1);
        break;
      }
    }
    this.forceUpdate();
  }

  render () {
    const { width, height, editMode } = this.props;
    console.log(this.state.rectangles)
    return (
      <>
        <Stage
          width={width}
          height={height}
          onMouseDown={this.checkDeselect}
          onTouchStart={this.checkDeselect}
        >
          <Layer>
            {this.state.rectangles.map((rect, i) => {
              return (
                <Rectangle
                  key={i}
                  shapeProps={rect}
                  isSelected={rect.id === this.state.selectedId}
                  onSelect={() => {
                    this.setState({
                      selectedId: rect.id
                    });
                  }}
                  onChange={(newAttrs) => {
                    const rects = this.state.rectangles.slice();
                    rects[i] = newAttrs;
                    this.setState({
                      rectangles: rects
                    });
                  }}
                  canvasSize={{
                    width: width,
                    height: height
                  }}
                  editMode={editMode}
                />
              );
            })}
          </Layer>
        </Stage>
      </>
    );
  }
}

export default CamTool;
