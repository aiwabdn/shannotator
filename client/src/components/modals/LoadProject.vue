<template>
  <a-modal :id="id">
    <template v-slot:header>
      Load Project
    </template>

    <template v-slot:body>
      <div class="form-group">
        <label for="projectList">Select a project</label>
        <input
          class="form-control"
          list="projectListOptions"
          id="projectList"
          v-model="selectedProject"
          placeholder="Select a project. Type to search..."
        />
        <datalist id="projectListOptions">
          <option v-for="(project, index) in projectList" v-bind:key="index" :value="project" />
        </datalist>
      </div>
    </template>

    <template v-slot:footer>
      <button class="btn btn-outline-secondary" data-dismiss="modal" @click="$emit('close')">
        Cancel
      </button>
      <button class="btn btn-outline-primary" data-dismiss="modal" @click="setProject()">
        Load
      </button>
    </template>
  </a-modal>
</template>

<script>
import aModal from "@/components/Modal.vue";

export default {
  name: "LoadProject",
  components: {
    aModal
  },

  props: {
    id: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      projectList: [],
      selectedProject: ""
    };
  },

  methods: {
    setProject() {
      this.$store.commit("setProjectName", this.selectedProject);
      this.$emit("close");
      this.$router.push({ name: "Project" });
    }
  },

  created() {
    const requestOptions = {
      method: "GET"
    };
    fetch("http://127.0.0.1:8000/saved_project_names", requestOptions)
      .then(response => response.json())
      .then(data => {
        this.projectList = data.data;
      });
  }
};
</script>
