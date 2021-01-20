<template>
  <v-row dense>
    <v-col cols="3" class="d-flex">
      <v-container>
        <v-row fill-height class="mb-2 halfrow">
          <v-col>
            <h2 class="ma-3">Files</h2>
            <list-selector
              :items="$store.state.projectFiles"
              :monitor="$store.state.currentFileIndex"
              @selected="setSelectedFile($event)"
            />
          </v-col>
        </v-row>

        <v-row fill-height class="mt-2 halfrow">
          <v-col cols="12">
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
              ref="defaultAttributeSet"
            />
            <div :style="{ visibility: editing ? 'visible' : 'hidden' }">
              <v-btn
                class="ma-3"
                color="teal lighten-4"
                @click="adding = !adding"
              >
                Add attribute
              </v-btn>
            </div>
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
            <update-attribute
              :flag="adding"
              @click:outside="adding = false"
              @close="adding = false"
            />
          </v-col>
        </v-row>
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
      refreshCounter: 0,
    };
  },

  watch: {
    editing: function (value) {
      if (!value) {
        this.$refs.defaultAttributeSet.forceRerender();
      }
    },
    adding: function (value) {
      if (!value) {
        this.$refs.defaultAttributeSet.forceRerender();
      }
    },
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
  height: 40pc;
  max-height: 40pc;
  overflow: auto;
  border: 2px solid black;
  border-radius: 5px;
}
</style>