<template>
  <v-toolbar dense class="text-center d-flex align-center justify-space-around">
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on" @click="zoomIn()">
          <v-icon>mdi-magnify-plus</v-icon>
        </v-btn>
      </template>
      <span>Zoom In</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on" @click="zoomOut()">
          <v-icon>mdi-magnify-minus</v-icon>
        </v-btn>
      </template>
      <span>Zoom Out</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
          @click="goPrevious()"
          :disabled="$store.state.currentFileIndex < 1"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
      <span>Previous</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
          @click="goNext()"
          :disabled="
            $store.state.currentFileIndex === $store.getters.getNumFiles - 1
          "
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </template>
      <span>Next</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon @click="save()" v-bind="attrs" v-on="on">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </template>
      <span>Save</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon @click="downloading = true" v-bind="attrs" v-on="on">
          <v-icon>mdi-download</v-icon>
        </v-btn>
      </template>
      <span>Download</span>
    </v-tooltip>

    <download :flag="downloading" @selected="formatSelected($event)" />

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on" @click="closeProject()">
          <v-icon>mdi-location-exit</v-icon>
        </v-btn>
      </template>
      <span>Close Project</span>
    </v-tooltip>
  </v-toolbar>
</template>

<script>
import Download from "@/components/forms/Download.vue";
import { downloadProject, saveAnnotations, CanvasManager } from "../utilities";

export default {
  name: "Toolbelt",

  data() {
    return {
      downloading: false,
    };
  },

  components: {
    Download,
  },

  methods: {
    save() {
      saveAnnotations();
    },

    formatSelected(fileFormat) {
      this.downloading = false;
      downloadProject(fileFormat);
    },

    zoomIn() {
      CanvasManager.zoomIn();
    },

    zoomOut() {
      CanvasManager.zoomOut();
    },

    goPrevious() {
      saveAnnotations();
      this.$store.commit("goPrevious");
      CanvasManager.loadImage();
    },

    goNext() {
      saveAnnotations();
      this.$store.commit("goNext");
      CanvasManager.loadImage();
    },

    closeProject() {
      this.$router.replace({ name: "Home" });
    },
  },
};
</script>
