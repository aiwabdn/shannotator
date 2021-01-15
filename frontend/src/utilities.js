import store from "@/store";
import _ from "lodash";

const REGION_SIZE_TOLERANCE = 5;
const ALLOWED_ZOOM_LEVELS = [1, 1.5, 2, 2.5, 3, 3.5, 4];
const SERVER_PORT = 8000;
const SERVER_ADDR = `${window.location.protocol}//${window.location.hostname}:${SERVER_PORT}`;

function downloadURI(uri, name) {
  const link = document.createElement("a");
  link.download = name;
  link.href = uri;
  link.click();
}

class CanvasManager {
  static canvas = null;

  static canvasCtx = null;

  static wrapper = null;

  static drawingBox = {
    active: false,
    left: 0,
    width: 0,
    height: 0
  };

  static selectedBox = null;

  static ZOOM_LEVEL_INDEX = 0;

  static originalImage = {
    width: 0,
    height: 0,
    url: null
  };

  static zoomTransform(arrayOfPoints) {
    return arrayOfPoints.map(p => p * ALLOWED_ZOOM_LEVELS[CanvasManager.ZOOM_LEVEL_INDEX]);
  }

  static reverseZoomTransform(arrayOfPoints) {
    return arrayOfPoints.map(p => p / ALLOWED_ZOOM_LEVELS[CanvasManager.ZOOM_LEVEL_INDEX]);
  }

  static zoomOut() {
    CanvasManager.ZOOM_LEVEL_INDEX =
      CanvasManager.ZOOM_LEVEL_INDEX === 0 ? 0 : CanvasManager.ZOOM_LEVEL_INDEX - 1;
    CanvasManager.setZoom();
  }

  static zoomIn() {
    CanvasManager.ZOOM_LEVEL_INDEX =
      CanvasManager.ZOOM_LEVEL_INDEX === ALLOWED_ZOOM_LEVELS.length - 1
        ? ALLOWED_ZOOM_LEVELS.length - 1
        : CanvasManager.ZOOM_LEVEL_INDEX + 1;
    CanvasManager.setZoom();
  }

  static setZoom() {
    const [width, height] = CanvasManager.zoomTransform([
      CanvasManager.originalImage.width,
      CanvasManager.originalImage.height
    ]);
    CanvasManager.imageElement.style.width = `${width}px`;
    CanvasManager.imageElement.style.height = `${height}px`;
    CanvasManager.canvas.width = width;
    CanvasManager.canvas.height = height;
    CanvasManager.drawRegions();
  }

  static drawRect(x, y, w, h, color) {
    CanvasManager.canvasCtx.strokeStyle = color ?? "#000000";
    CanvasManager.canvasCtx.strokeRect(x, y, w, h);
  }

  static drawRegions() {
    CanvasManager.canvasCtx.clearRect(
      0,
      0,
      CanvasManager.canvas.width,
      CanvasManager.canvas.height
    );
    store.getters.getRegions().forEach(region => {
      // upscale points by current zoom level
      const [x1, y1, x2, y2] = CanvasManager.zoomTransform(region.points);
      // get color for region by coloring attribute
      const color = store.getters.getRegionValueColor(
        region.attributes[store.state.coloringAttribute]
      );
      CanvasManager.drawRect(x1, y1, x2 - x1, y2 - y1, color);
    });
  }

  static registerImageElement(imageElement) {
    CanvasManager.imageElement = imageElement;
  }

  static registerCanvas(canvasElement) {
    CanvasManager.canvas = canvasElement;
    CanvasManager.canvasCtx = canvasElement.getContext("2d");
    CanvasManager.wrapper = canvasElement.parentElement;
  }

  static refreshCanvas(imageUrl) {
    document.documentElement.scrollTop = 0;
    CanvasManager.ZOOM_LEVEL_INDEX = 0;
    CanvasManager.canvasCtx.clearRect(
      0,
      0,
      CanvasManager.canvas.width,
      CanvasManager.canvas.height
    );
    if (imageUrl === undefined) {
      CanvasManager.canvasCtx.font = "30px Helvetica";
      CanvasManager.canvasCtx.fillText("Select a file to view", 10, 50);
    } else {
      const img = new Image();
      img.src = imageUrl;
      img.onload = () => {
        CanvasManager.canvas.width = img.width;
        CanvasManager.canvas.height = img.height;
        CanvasManager.imageElement.style.width = `${img.width}px`;
        CanvasManager.imageElement.style.height = `${img.height}px`;
        CanvasManager.originalImage = {
          width: img.width,
          height: img.height,
          url: imageUrl
        };
      };
    }
  }

  static handleMouseDown(e) {
    CanvasManager.drawingBox = {
      active: true,
      left:
        e.pageX -
        CanvasManager.wrapper.getBoundingClientRect().left +
        CanvasManager.wrapper.scrollLeft,
      top:
        e.pageY -
        CanvasManager.wrapper.getBoundingClientRect().top +
        CanvasManager.wrapper.scrollTop,
      width: 0,
      height: 0
    };
  }

  static handleMouseMove(e) {
    if (!CanvasManager.drawingBox.active) return;
    CanvasManager.handleScroll(e);
    const currentLeft =
      e.pageX -
      CanvasManager.wrapper.getBoundingClientRect().left +
      CanvasManager.wrapper.scrollLeft;
    const currentTop =
      e.pageY - CanvasManager.wrapper.getBoundingClientRect().top + CanvasManager.wrapper.scrollTop;
    CanvasManager.canvasCtx.clearRect(
      0,
      0,
      CanvasManager.canvas.width,
      CanvasManager.canvas.height
    );
    CanvasManager.drawingBox.width = currentLeft - CanvasManager.drawingBox.left;
    CanvasManager.drawingBox.height = currentTop - CanvasManager.drawingBox.top;
    CanvasManager.drawRect(
      CanvasManager.drawingBox.left,
      CanvasManager.drawingBox.top,
      CanvasManager.drawingBox.width,
      CanvasManager.drawingBox.height,
      store.getters.getCurrentRegionColor()
    );
  }

  static handleMouseUp(e) {
    const currentLeft =
      e.pageX -
      CanvasManager.wrapper.getBoundingClientRect().left +
      CanvasManager.wrapper.scrollLeft;
    const currentTop =
      e.pageY - CanvasManager.wrapper.getBoundingClientRect().top + CanvasManager.wrapper.scrollTop;
    let bbox = [
      Math.min(CanvasManager.drawingBox.left, currentLeft),
      Math.min(CanvasManager.drawingBox.top, currentTop),
      Math.max(CanvasManager.drawingBox.left, currentLeft),
      Math.max(CanvasManager.drawingBox.top, currentTop)
    ];

    // downscale by zoom level
    bbox = CanvasManager.reverseZoomTransform(bbox);
    if (!CanvasManager.isBoxSmall(bbox)) {
      store.commit("addBox", bbox);
    }
    CanvasManager.drawRegions();

    const containingBox = CanvasManager.findSmallestContainingBox(e);
    store.commit("setSelectedBox", containingBox);
    if (containingBox) {
      CanvasManager.showAsSelected(containingBox);
    }

    CanvasManager.drawingBox = {
      active: false,
      left: 0,
      top: 0,
      width: 0,
      height: 0
    };
  }

  static showAsSelected(bbox) {
    const [x1, y1, x2, y2] = CanvasManager.zoomTransform(bbox);
    CanvasManager.canvasCtx.clearRect(x1, y1, x2 - x1, y2 - y1);
    CanvasManager.drawRect(x1, y1, x2 - x1, y2 - y1, "#FF0000");
  }

  static isBoxSmall(bbox) {
    const width = bbox[2] - bbox[0];
    const height = bbox[3] - bbox[1];
    const isNotWide = width < REGION_SIZE_TOLERANCE;
    const isNotHigh = height < REGION_SIZE_TOLERANCE;
    return isNotWide && isNotHigh;
  }

  static findSmallestContainingBox(e) {
    const detectedLeft = e.pageX - CanvasManager.canvas.getBoundingClientRect().left; // + CanvasManager.wrapper.scrollLeft;
    const detectedTop = e.pageY - CanvasManager.canvas.getBoundingClientRect().top; // + CanvasManager.wrapper.scrollTop;
    const [currentLeft, currentTop] = CanvasManager.reverseZoomTransform([
      detectedLeft,
      detectedTop
    ]);
    const picked = _.filter(store.getters.getRegions(), function b(box) {
      return (
        box.points[0] <= currentLeft &&
        box.points[1] <= currentTop &&
        box.points[2] >= currentLeft &&
        box.points[3] >= currentTop
      );
    });
    let result = null;
    // console.log("picked", JSON.stringify(picked));
    if (picked.length === 0) {
      result = null;
    } else if (picked.length === 1) {
      result = picked[0].points;
    } else {
      result = _.minBy(picked, function b(box) {
        return (box.points[2] - box.points[0]) * (box.points[3] - box.points[1]);
      }).points;
    }
    // console.log("result", result);
    return result;
  }

  static handleScroll(event) {
    // https://www.bennadel.com/blog/3460-automatically-scroll-the-window-when-the-user-approaches-the-viewport-edge-in-javascript.htm

    // Get the viewport-relative coordinates of the mousemove event.
    let timer = null;
    const bwrapper = CanvasManager.wrapper;
    const viewportX = event.pageX;
    const viewportY = event.pageY;

    // Get the viewport dimensions.
    const viewportWidth = bwrapper.getBoundingClientRect().width;
    const viewportHeight = bwrapper.getBoundingClientRect().height;

    const edgeTop = bwrapper.getBoundingClientRect().top;
    const edgeLeft = bwrapper.getBoundingClientRect().left;
    const edgeBottom = bwrapper.getBoundingClientRect().bottom;
    const edgeRight = bwrapper.getBoundingClientRect().right;

    const isInLeftEdge = viewportX < edgeLeft;
    const isInRightEdge = viewportX > edgeRight;
    const isInTopEdge = viewportY < edgeTop;
    const isInBottomEdge = viewportY > edgeBottom;

    if (!(isInLeftEdge || isInRightEdge || isInTopEdge || isInBottomEdge)) {
      clearTimeout(timer);
      return;
    }

    const documentWidth = CanvasManager.canvas.getBoundingClientRect().width;
    const documentHeight = CanvasManager.canvas.getBoundingClientRect().height;

    const maxScrollX = documentWidth - viewportWidth;
    const maxScrollY = documentHeight - viewportHeight;

    function adjustWindowScroll() {
      const currentScrollX = bwrapper.scrollLeft;
      const currentScrollY = bwrapper.scrollTop;

      const canScrollUp = currentScrollY > 0;
      const canScrollDown = currentScrollY < maxScrollY;
      const canScrollLeft = currentScrollX > 0;
      const canScrollRight = currentScrollX < maxScrollX;

      let nextScrollX = currentScrollX;
      let nextScrollY = currentScrollY;

      const maxStep = 10;
      const intensity = 1;

      if (isInLeftEdge && canScrollLeft) {
        nextScrollX -= maxStep * intensity;
      } else if (isInRightEdge && canScrollRight) {
        nextScrollX += maxStep * intensity;
      }

      if (isInTopEdge && canScrollUp) {
        nextScrollY -= maxStep * intensity;
      } else if (isInBottomEdge && canScrollDown) {
        nextScrollY += maxStep * intensity;
      }

      nextScrollX = Math.max(0, Math.min(maxScrollX, nextScrollX));
      nextScrollY = Math.max(0, Math.min(maxScrollY, nextScrollY));

      if (nextScrollX !== currentScrollX || nextScrollY !== currentScrollY) {
        bwrapper.scrollTo(nextScrollX, nextScrollY);
        return true;
      }
      return false;
    }

    (function checkForWindowScroll() {
      clearTimeout(timer);

      if (adjustWindowScroll()) {
        timer = setTimeout(checkForWindowScroll, 1000);
      }
    })();
  }

  static handleKeyPress(e) {
    if (store.state.currentSelectionIndex > -1) {
      switch (e.key) {
        case "d":
          if (!store.state.isEditing) {
            store.commit("removeBox", store.state.currentSelectionIndex);
            CanvasManager.drawRegions();
          }
          break;
        default:
          console.log("pressed ", e.key);
      }
    }
  }
}

// eslint-disable-next-line
export { CanvasManager, downloadURI, SERVER_ADDR };
