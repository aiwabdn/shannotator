<template>
  <a-modal :id="id">
    <template v-slot:header>
      Create New Connection
    </template>
    <template v-slot:body>
      <form>
        <div class="form-group">
          <label for="connectionName">Name</label>
          <input
            type="text"
            class="form-control"
            id="connectionName"
            v-model="connectionName"
            placeholder="Name for the new connection"
            aria-label="connectionNameField"
            aria-describedby="connection-name-field"
          />
        </div>

        <div class="form-group">
          <label for="storageList">Storage Type</label>
          <input
            class="form-control"
            list="storageOptions"
            id="storageList"
            v-model="selectedStorage"
            placeholder="Type to search..."
            @change="showParams = true"
          />
          <datalist id="storageOptions">
            <option
              v-for="(name, index) in Object.keys(supportedStorages)"
              v-bind:key="index"
              :value="name"
            />
          </datalist>
        </div>

        <div v-if="showParams">
          <div
            v-for="(param, index) in supportedStorages[selectedStorage]"
            v-bind:key="index"
            class="form-group"
          >
            <label :for="`${param.name}field`">{{ param.name }}</label>
            <input
              type="text"
              class="form-control"
              :id="`${param.name}field`"
              :aria-label="`${param.name}label`"
              :aria-describedby="`${param.name}-label`"
              :placeholder="param.description"
              required
            />
          </div>
        </div>
      </form>
    </template>

    <template v-slot:footer>
      <button class="btn btn-outline-secondary" data-dismiss="modal" @click="$emit('close')">
        Cancel
      </button>
      <button class="btn btn-outline-primary" data-dismiss="modal" @click="setParams()">
        Save
      </button>
    </template>
  </a-modal>
</template>

<script>
import aModal from "@/components/Modal.vue";

export default {
  name: "CreateNewConnection",
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
      supportedStorages: {
        Local: [{ name: "Path", description: "Path to local directory of images" }]
      },
      showParams: false,
      selectedStorage: "",
      connectionName: ""
    };
  },

  methods: {
    setSelectedStorage(event) {
      this.showParams = true;
      this.selectedStorage = event.target.value;
    },

    setSupportedStorages(data) {
      this.supportedStorages = data;
    },

    setParams() {
      console.log("setting");
      const parameters = [];
      this.supportedStorages[this.selectedStorage].forEach(data => {
        parameters.push({
          name: data.name,
          value: document.getElementById(`${data.name}field`).value
        });
      });

      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          name: this.connectionName,
          storage_type: this.selectedStorage,
          params: parameters
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      fetch("http://127.0.0.1:8000/create_connection", requestOptions).catch(e => {
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

    fetch("http://127.0.0.1:8000/supported_storages", requestOptions)
      .then(response => response.json())
      .then(data => this.setSupportedStorages(data.storage_types))
      .catch(e => {
        console.log(e);
        return e;
      });
  }
};
</script>
