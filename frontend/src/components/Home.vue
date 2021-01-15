<template>
  <!-- <div class="d-flex align-items-center min-vh-100"> -->
  <div class="d-flex justify-content-center align-items-center min-vh-100" style="height:100%;">
    <div class="container">
      <div class="col-md-8 offset-md-2">
        <h1>AMMOtator Home</h1>

        <button class="btn btn-primary" data-toggle="modal" data-target="#newconnectionmodal">
          Create New Connection
        </button>
        <create-new-connection id="newconnectionmodal"></create-new-connection>
        <br />

        <button class="btn btn-primary" data-toggle="modal" data-target="#newprojectmodal">
          Create New Project
        </button>
        <create-new-project id="newprojectmodal"></create-new-project>
        <br />

        <button class="btn btn-primary" data-toggle="modal" data-target="#loadprojectmodal">
          Load Project
        </button>
        <load-project id="loadprojectmodal"></load-project>
        <br />
      </div>
    </div>
  </div>
</template>

<script>
import CreateNewConnection from "@/components/modals/CreateNewConnection.vue";
import CreateNewProject from "@/components/modals/CreateNewProject.vue";
import LoadProject from "@/components/modals/LoadProject.vue";

export default {
  name: "Home",

  components: {
    CreateNewConnection,
    CreateNewProject,
    LoadProject
  },

  mounted() {
    this.$store.commit("reset");
  }
};
</script>

<style scoped>
button {
  margin: 5px;
  width: 50%;
  min-width: 200px;
}
/* .app {
  background-color: #ccf7e2;
  border-radius: 5px;
  margin: 0 auto;
  max-width: 800px;
  min-width: 500px;
  width: 50%;
  padding: 10px;
  min-height: 100%;
  display: flex;
  align-items: center;
} */

.container {
  background-color: #ccf7e2;
  border-radius: 5px;
  display: inline-block;
  vertical-align: middle;
}
</style>
