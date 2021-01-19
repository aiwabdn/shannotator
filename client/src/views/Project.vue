<template>
  <v-row dense>
    <v-col cols="3" class="d-flex" style="flex-direction: column">
      <v-container>
        <!-- <v-card style="height: 50%; max-height: 1000px; overflow: auto">
        <v-card-text> -->
        <!-- <div class="halfrow"> -->
        <v-row class="ma3 halfrow">
          <v-col>
            <h2 class="ma-3">Files</h2>
            <list-selector
              :items="$store.state.projectFiles"
              :monitor="$store.state.currentFileIndex"
              @selected="setSelectedFile($event)"
            />
          </v-col>
        </v-row>
        <!-- </div> -->
        <!-- </v-card-text> -->
        <!-- </v-card> -->
        <!-- <v-card style="height: 50%; max-height: 1000px; overflow: auto">
        <v-card-text>
          <template> -->
        <!-- <div class="halfrow"> -->

        <v-row class="ma3 halfrow">
          <v-col>
            <v-container fluid>
              <h2 class="ma-3">
                Default Attributes
                <v-btn
                  icon
                  right
                  x-small
                  v-if="!editing"
                  type="button"
                  @click="editing = !editing"
                  ><v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  right
                  x-small
                  v-if="editing"
                  type="button"
                  @click="editing = !editing"
                  ><v-icon>mdi-content-save</v-icon>
                </v-btn>
              </h2>
              <attribute-set
                :editing="editing"
                type="default"
                @change="setDefaultAttributeValue"
              />
              <v-row v-if="editing">
                <v-btn block color="teal lighten-4" @click="adding = !adding">
                  Add attribute
                </v-btn>
                <update-attribute
                  v-if="editing"
                  :flag="adding"
                  @click:outside="adding = false"
                  @close="adding = false"
                />
              </v-row>
              <v-select
                outlined
                full-width
                clearable
                dense
                label="Color region by"
                placeholder="None"
                :items="$store.getters.getRadioAttributeNames()"
                @change="coloringSelected"
              />
            </v-container>
          </v-col>
        </v-row>
        <!-- </div> -->
        <!-- </template>
        </v-card-text>
      </v-card> -->
      </v-container>
    </v-col>
    <v-col cols="9">
      <toolbelt />
      <annotation-canvas ref="anno" />
    </v-col>
  </v-row>
</template>

<script>
import Toolbelt from "@/components/Toolbelt.vue";
import { CanvasManager, SERVER_ADDR, sleep } from "../utilities";
import ListSelector from "../components/ListSelector.vue";
import AnnotationCanvas from "../components/AnnotationCanvas.vue";
import AttributeSet from "../components/AttributeSet.vue";
import UpdateAttribute from "../components/forms/UpdateAttribute.vue";

export default {
  name: "Project",

  data() {
    return {
      editing: false,
      adding: false,
    };
  },

  components: {
    Toolbelt,
    ListSelector,
    AnnotationCanvas,
    AttributeSet,
    UpdateAttribute,
  },

  methods: {
    log(event) {
      console.log(event);
    },

    coloringSelected(event) {
      this.$store.commit("setColoringAttribute", event);
      CanvasManager.drawRegions();
    },

    setDefaultAttributeValue(event) {
      this.$store.commit("setDefaultAttribute", event);
    },

    setSelectedFile(fileIndex) {
      console.log(fileIndex);
      this.$store.commit(
        "setCurrentFileIndex",
        this.$store.state.projectFiles[fileIndex]
      );
      CanvasManager.loadImage();
    },
  },

  created() {
    fetch(`${SERVER_ADDR}/load_project/${this.$store.state.projectName}`, {
      method: "POST",
    })
      .then((dummy) => {
        console.log(dummy.json());
        const requestOptions = {
          method: "GET",
        };
        fetch(
          `${SERVER_ADDR}/project_settings/${this.$store.state.projectName}`,
          requestOptions
        )
          .then((response) => response.json())
          .then((data) => {
            this.$store.commit("setProjectSettings", data.settings);
            sleep(100);
          });
        fetch(
          `${SERVER_ADDR}/project_files/${this.$store.state.projectName}`,
          requestOptions
        )
          .then((response) => response.json())
          .then((data) => {
            this.$store.commit("setProjectFiles", data.data);
          });
      })
      .catch((e) => {
        console.log(e);
        return e;
      });
  },
};
</script>

<style>
.halfrow {
  height: 50%;
  max-height: 1000px;
  overflow: auto;
  border: 1px solid black;
  border-radius: 5px;
}
</style>