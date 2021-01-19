<template>
  <v-container fluid id="anno-container">
    <div class="wrapper" id="wrapper">
      <img
        :src="$store.state.currentFileObject"
        class="source-image"
        id="anno-img"
      />
      <canvas
        class="overlay-canvas"
        id="anno-canvas"
        ref="canvas"
        @mousedown="startDrawing"
        @mousemove="whileDrawing"
        @mouseup="stopDrawing"
      >
      </canvas>
      <div
        v-if="$store.state.currentSelectionIndex > -1"
        v-bind:key="$store.state.currentSelectionIndex"
      >
        <Annotation
          id="selection"
          :left="$store.getters.getSelectionPoints()[2]"
          :top="$store.getters.getSelectionPoints()[3]"
        />
      </div>
    </div>
  </v-container>
</template>

<script>
import Annotation from "@/components/Annotation.vue";
import { CanvasManager } from "../utilities";

export default {
  name: "AnnotationCanvas",

  components: {
    Annotation,
  },

  methods: {
    startDrawing(e) {
      CanvasManager.handleMouseDown(e);
    },

    whileDrawing(e) {
      CanvasManager.handleMouseMove(e);
    },

    stopDrawing(e) {
      CanvasManager.handleMouseUp(e);
    },
  },

  mounted() {
    CanvasManager.registerImageElement(document.getElementById("anno-img"));
    CanvasManager.registerCanvas(document.getElementById("anno-canvas"));
    CanvasManager.refreshCanvas();
    window.addEventListener("keyup", CanvasManager.handleKeyPress);
  },
};
</script>

<style>
.wrapper {
  position: relative;
  padding: 0px 5px 5px 0px;
}
.source-image {
  position: absolute;
  left: 0px;
  top: 0px;
}
.overlay-canvas {
  position: absolute;
  left: 0px;
  top: 0px;
  z-index: 10;
}
#anno-container {
  border: 2px solid gray;
  border-radius: 5px;
  height: 95%;
  overflow: auto;
}
</style>