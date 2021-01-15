<template>
  <a-modal :id="id">
    <template v-slot:header>
      Create New Project
    </template>

    <template v-slot:body>
      <form>
        <div class="form-group">
          <label for="projectName">Name</label>
          <input
            type="text"
            class="form-control"
            id="projectName"
            v-model="projectName"
            placeholder="Name for the new project"
          />
        </div>

        <div class="form-group">
          <label for="connectionList">Source connection</label>
          <input
            class="form-control"
            list="connectionOptions"
            id="connectionList"
            v-model="sourceConnection"
            placeholder="Type to search..."
          />
          <datalist id="connectionOptions">
            <option v-for="(name, index) in storedConnections" v-bind:key="index" :value="name" />
          </datalist>
        </div>

        <div class="form-group">
          <label for="sourcePath">Path</label>
          <input
            type="text"
            class="form-control"
            id="sourcePath"
            placeholder="Path to source directory"
            v-model="sourcePath"
          />
        </div>
      </form>
    </template>

    <template v-slot:footer>
      <button class="btn btn-outline-secondary" data-dismiss="modal" @click="$emit('close')">
        Cancel
      </button>
      <button class="btn btn-outline-primary" data-dismiss="modal" @click="createNewProject()">
        Create
      </button>
    </template>
  </a-modal>
</template>

<script>
import aModal from "@/components/Modal.vue";

export default {
  name: "CreateNewProject",
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
      storedConnections: ["Local"],
      sourceConnection: "",
      sourcePath: "",
      projectName: ""
    };
  },
  methods: {
    setSourceConnection(event) {
      this.sourceConnection = event.target.value;
    },
    setStoredConnections(data) {
      this.storedConnections = data;
    },
    createNewProject() {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          name: this.projectName,
          connection: this.sourceConnection,
          path: this.sourcePath
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      fetch("http://127.0.0.1:8000/create_project", requestOptions)
        .then(response => response.json())
        .catch(e => {
          console.log(e);
          return e;
        });
      this.$emit("close");
    }
  },
  created() {
    const requestOptions = {
      method: "GET"
    };
    fetch("http://127.0.0.1:8000/saved_connection_names", requestOptions)
      .then(response => response.json())
      .then(data => this.setStoredConnections(data.data))
      .catch(e => {
        console.log(e);
        return e;
      });
  }
};
</script>
