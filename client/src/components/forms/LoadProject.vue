<template>
  <!-- <v-row justify="center"> -->
  <v-dialog v-model="showing" width="30%" max-width="50%">
    <v-card>
      <v-card-title>Load Project</v-card-title>
      <v-card-text>
        <!-- <v-form> -->
        <v-select
          outlined
          dense
          v-model="name"
          :items="projects"
          :error-messages="selectErrors"
          label="Project Name"
          placeholder="Select a project..."
          required
        ></v-select>
        <!-- </v-form> -->
      </v-card-text>
      <v-divider class="mt-12"></v-divider>
      <v-card-actions>
        <v-btn color="red lighten-4" @click="showing = false"> Cancel </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="teal lighten-4" @click="loadProject()"> Load </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <!-- </v-row> -->
</template>

<script>
import { required } from "vuelidate/lib/validators";
import { SERVER_ADDR } from "../../utilities";

export default {
  name: "CreateProject",

  props: {
    flag: {
      type: Boolean,
      required: true
    }
  },

  data() {
    return {
      name: "",
      projects: []
    };
  },

  validations: {
    name: {
      required
    }
  },

  methods: {
    loadProject() {
      this.$store.commit("setProjectName", this.name);
      this.showing = false;
      this.$router.push({ name: "Project" });
    }
  },

  mounted() {
    const requestOptions = {
      method: "GET"
    };
    fetch(`${SERVER_ADDR}/saved_project_names`, requestOptions)
      .then(response => response.json())
      .then(data => {
        this.projects = data.data;
      });
  },

  computed: {
    showing: {
      get: function() {
        return this.flag;
      },
      set: function(value) {
        if (!value) {
          this.$emit("close");
        }
      }
    },
    selectErrors() {
      const errors = [];
      //   if (!this.$v.select.$dirty) return errors;
      //   !this.$v.select.required && errors.push("Item is required");
      return errors;
    }
  }
};
</script>
