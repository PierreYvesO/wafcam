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

const CamTool = (props) => {
  const { width, height, editMode, initialRectangles } = props;
  const [rectangles, setRectangles] = React.useState(initialRectangles);
  const [selectedId, selectShape] = React.useState(null);

  const checkDeselect = (e) => {
    // deselect when clicked on empty area
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      selectShape(null);
    }
  };

  return (
    <>
      <Stage
        width={width}
        height={height}
        onMouseDown={checkDeselect}
        onTouchStart={checkDeselect}
      >
        <Layer>
          {rectangles.map((rect, i) => {
            return (
              <Rectangle
                key={i}
                shapeProps={rect}
                isSelected={rect.id === selectedId}
                onSelect={() => {
                  selectShape(rect.id);
                }}
                onChange={(newAttrs) => {
                  const rects = rectangles.slice();
                  rects[i] = newAttrs;
                  setRectangles(rects);
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

export default CamTool;
