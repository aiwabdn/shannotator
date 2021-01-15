<template>
  <div class="d-flex align-items-center min-vh-100">
    <div class="container-fluid">
      <h1>{{ $store.state.projectName }}</h1>
      <div class="row gy-1 border">
        <div class="col-2 border">
          <div class="row" style="max-height:50%; overflow:auto;">
            <div class="col border">
              <h5 class="display-5">Files</h5>
              <div class="list-group" role="tablist">
                <button
                  type="button"
                  class="d-block list-group-item list-group-item-action text-left small"
                  role="tab"
                  data-bs-toggle="list"
                  v-for="(file, idx) in $store.state.projectFiles"
                  v-bind:key="idx"
                  v-on:click="selected(file)"
                  v-bind:class="{ active: isSelected(file) }"
                >
                  {{ file }}
                </button>
              </div>
            </div>
          </div>

          <div class="row" style="max-height:50%; overflow:auto;">
            <div class="col border">
              <Settings />
            </div>
          </div>
        </div>

        <div class="col-10">
          <Anno ref="anno" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Settings from "@/components/Settings.vue";
import Anno from "@/components/Anno.vue";
import { SERVER_ADDR } from "../utilities";

export default {
  name: "Project",
  components: {
    Anno,
    Settings
  },

  methods: {
    selected(file) {
      this.$refs.anno.saveAnnotations();
      this.$store.commit("setCurrentFileIndex", file);
      this.$refs.anno.loadImage();
    },

    isSelected(file) {
      return file === this.$store.getters.getCurrentFileName;
    }
  },

  created() {
    fetch(`${SERVER_ADDR}/load_project/${this.$store.state.projectName}`, {
      method: "POST"
    })
      .then(dummy => {
        console.log(dummy.json());
        const requestOptions = {
          method: "GET"
        };
        fetch(`${SERVER_ADDR}/project_settings/${this.$store.state.projectName}`, requestOptions)
          .then(response => response.json())
          .then(data => {
            this.$store.commit("setProjectSettings", data.settings);
          });
        fetch(`${SERVER_ADDR}/project_files/${this.$store.state.projectName}`, requestOptions)
          .then(response => response.json())
          .then(data => {
            this.$store.commit("setProjectFiles", data.data);
          });
      })
      .catch(e => {
        console.log(e);
        return e;
      });
  }
};
</script>
