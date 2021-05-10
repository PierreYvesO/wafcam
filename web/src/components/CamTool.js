import React from 'react';
import { Stage, Rect, Layer, Transformer, Label, Text, Tag } from 'react-konva';

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
      <Label
        x={shapeProps.x + 5}
        y={shapeProps.y + 5}
        width={shapeProps.width}
        height={25}
        onClick={(evt) => {
          if (editMode) {
            var textarea = document.createElement('textarea');
            var camTool = document.querySelector(".camTool");
            camTool.appendChild(textarea);
            textarea.value = shapeProps.name;
            textarea.style.position = 'absolute';
            textarea.style.top = evt.target.parent.attrs.y + 'px';
            textarea.style.left = evt.target.parent.attrs.x + 'px';
            textarea.style.width = (evt.target.parent.attrs.width - 10) + 'px';
            textarea.style.height = 25 + 'px';
            textarea.style.fontSize = 20 + 'px';
            textarea.style.border = 'none';
            textarea.style.padding = '0px';
            textarea.style.margin = '0px';
            textarea.style.overflow = 'hidden';
            textarea.style.outline = 'none';
            textarea.style.resize = 'none';
            textarea.style.transformOrigin = 'left top';
            textarea.focus();
            function removeTextarea() {
              camTool.removeChild(textarea);
              window.removeEventListener('click', handleOutsideClick);
            }
            textarea.addEventListener('keydown', function (e) {
              // hide on enter
              // but don't hide on shift + enter
              if (e.keyCode === 13 && !e.shiftKey) {
                shapeProps.name = textarea.value;
                removeTextarea();
              }
              // on esc do not set value back to node
              if (e.keyCode === 27) {
                removeTextarea();
              }
            });
            function handleOutsideClick(e) {
              if (e.target !== textarea) {
                shapeProps.name = textarea.value;
                removeTextarea();
              }
            }
            setTimeout(() => {
              window.addEventListener('click', handleOutsideClick);
            });
          }
        }}
      >
        <Tag
          fill={editMode ? '#0f0' : '#f00'}
          opacity={0.3}
        />
        <Text
          text={shapeProps.name}
          fontSize={20}
        />
      </Label>
    </React.Fragment>
  );
};

class CamTool extends React.Component {
  state = {
    rectangles: this.props.initialRectangles,
    selectedId: null,
    countNewRectangles: 0
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
      id: "new" + (this.state.countNewRectangles + 1),
      draggable: this.props.editMode
    });
    this.setState({
      countNewRectangles: this.state.countNewRectangles + 1,
      selectedId: "new" + (this.state.countNewRectangles + 1)
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
