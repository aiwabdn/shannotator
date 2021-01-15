<template>
  <div class="container-fluid">
    <Toolbar
      @zoomin="zoomIn"
      @zoomout="zoomOut"
      @goprevious="goPrevious"
      @gonext="goNext"
      @save="saveAnnotations"
      @close="closeProject"
      @download="downloadProject"
    />
    <div class="wrapper" id="wrapper">
      <img :src="targetFile" class="source-image" id="anno-img" />
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
  </div>
</template>

<script>
import Annotation from "@/components/Annotation.vue";
import Toolbar from "@/components/Toolbar.vue";
import { SERVER_ADDR, downloadURI, CanvasManager } from "../utilities";

export default {
  name: "Anno",

  components: {
    Toolbar,
    Annotation
  },

  data() {
    return {
      filename: this.$store.getters.getCurrentFileName,
      targetFile: ""
    };
  },

  methods: {
    close() {
      this.$emit("close");
    },

    zoomIn() {
      CanvasManager.zoomIn();
    },

    zoomOut() {
      CanvasManager.zoomOut();
    },

    async saveAnnotations() {
      if (this.$store.state.currentFileIndex > -1) {
        const requestOptions = {
          method: "POST",
          body: JSON.stringify({
            project: this.$store.state.projectName,
            path: this.$store.getters.getCurrentFileName,
            annotations: this.$store.state.currentAnnotations
          }),
          headers: { "Content-type": "application/json; charset=UTF-8" }
        };
        await fetch(`${SERVER_ADDR}/save_annotation`, requestOptions);
      }
    },

    async downloadProject(fileFormat) {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          project: this.$store.state.projectName,
          format: fileFormat
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      await fetch(`${SERVER_ADDR}/download_project`, requestOptions)
        .then(response => response.blob())
        .then(data => {
          const dataURL = URL.createObjectURL(data);
          downloadURI(dataURL, `${this.$store.state.projectName}.${fileFormat}`);
        });
    },

    goPrevious() {
      this.saveAnnotations();
      this.$store.commit("goPrevious");
      this.loadImage();
    },

    goNext() {
      this.saveAnnotations();
      this.$store.commit("goNext");
      this.loadImage();
    },

    closeProject() {
      this.$router.replace({ name: "Home" });
    },

    startDrawing(e) {
      CanvasManager.handleMouseDown(e);
    },

    whileDrawing(e) {
      CanvasManager.handleMouseMove(e);
    },

    stopDrawing(e) {
      CanvasManager.handleMouseUp(e);
    },

    async loadImage() {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          project: this.$store.state.projectName,
          path: this.$store.getters.getCurrentFileName
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      await fetch(`${SERVER_ADDR}/file_request`, requestOptions)
        .then(response => response.blob())
        .then(image => {
          const imgUrl = URL.createObjectURL(image);
          CanvasManager.refreshCanvas(imgUrl);
          this.targetFile = imgUrl;
        });
      await fetch(`${SERVER_ADDR}/annotation_request`, requestOptions)
        .then(response => response.json())
        .then(data => {
          this.$store.commit("setCurrentAnnotations", data);
          CanvasManager.drawRegions();
        });
    }
  },

  mounted() {
    CanvasManager.registerImageElement(document.getElementById("anno-img"));
    CanvasManager.registerCanvas(document.getElementById("anno-canvas"));
    CanvasManager.refreshCanvas();
    window.addEventListener("keyup", CanvasManager.handleKeyPress);
  }
};
</script>

<style>
.wrapper {
  position: absolute;
  left: 50px;
  top: 50px;
  width: 90%;
  height: 90%;
  overflow: auto;
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
  z-index: 2;
}
</style>
