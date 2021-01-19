<template>
  <!-- <v-container id="home"> -->
  <div style="width: 100%">
    <div>
      <v-btn
        class="homebtn"
        x-large
        color="teal lighten-2"
        dark
        @click="newConnection = true"
      >
        Create New Connection
      </v-btn>
    </div>
    <div>
      <v-btn
        class="homebtn"
        x-large
        color="teal lighten-2"
        dark
        @click="newProject = true"
      >
        Create New Project
      </v-btn>
    </div>
    <div>
      <v-btn
        class="homebtn"
        x-large
        color="teal lighten-2"
        dark
        @click="loadProject = true"
      >
        Load Project
      </v-btn>
    </div>
    <create-connection
      :flag="newConnection"
      @click:outside="newConnection = false"
      @close="newConnection = false"
    />
    <create-project
      :flag="newProject"
      @click:outside="newProject = false"
      @close="newProject = false"
    />
    <load-project
      :flag="loadProject"
      @click:outside="loadProject = false"
      @close="loadProject = false"
    />
    <!-- </v-container> -->
  </div>
</template>

<script>
import CreateConnection from "@/components/forms/CreateConnection.vue";
import CreateProject from "@/components/forms/CreateProject.vue";
import LoadProject from "@/components/forms/LoadProject.vue";

export default {
  name: "Home",

  components: {
    CreateConnection,
    CreateProject,
    LoadProject,
  },

  data() {
    return {
      newConnection: false,
      newProject: false,
      loadProject: false,
    };
  },

  methods: {},

  mounted() {
    this.$store.commit("reset");
  },
};
</script>

<style scoped>
.homebtn {
  margin: 10px;
  width: 30%;
  min-width: 200px;
}
</style>
