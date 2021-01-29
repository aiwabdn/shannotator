<template>
  <v-row justify="center">
    <v-dialog v-model="showing" width="30%" max-width="50%">
      <v-card>
        <v-card-title>Create New Project</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              outlined
              dense
              v-model="name"
              :error-messages="nameErrors"
              label="Name"
              placeholder="Name for new project"
              required
            ></v-text-field>
            <v-select
              outlined
              dense
              v-model="connectionName"
              :items="connections"
              :error-messages="selectErrors"
              label="Connection Name"
              placeholder="Select a stored connection"
              required
            ></v-select>
            <v-text-field
              outlined
              dense
              v-model="path"
              :error-messages="pathErrors"
              label="Source Path"
              placeholder="Path to source directory"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-divider class="mt-12"></v-divider>
        <v-card-actions>
          <v-btn color="red lighten-4" @click="showing = false"> Cancel </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="teal lighten-4" @click="createNewProject()">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
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
      connectionName: "",
      connections: ["Local"],
      path: ""
    };
  },

  validations: {
    name: {
      required
    },
    connectionName: {
      required
    },
    path: {
      required
    }
  },

  methods: {
    createNewProject() {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          name: this.name,
          connection: this.connectionName,
          path: this.path
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      fetch(`${SERVER_ADDR}/create_project`, requestOptions)
        .then(response => response.json())
        .catch(e => {
          console.log(e);
          return e;
        });
      this.showing = false;
    }
  },

  mounted() {
    const requestOptions = {
      method: "GET"
    };
    fetch(`${SERVER_ADDR}/saved_connection_names`, requestOptions)
      .then(response => response.json())
      .then(data => (this.connections = data))
      .catch(e => {
        console.log(e);
        return e;
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
    pathErrors() {
      const errors = [];
      return errors;
    },
    selectErrors() {
      const errors = [];
      //   if (!this.$v.select.$dirty) return errors;
      //   !this.$v.select.required && errors.push("Item is required");
      return errors;
    },
    nameErrors() {
      const errors = [];
      //   if (!this.$v.name.$dirty) return errors;
      //   !this.$v.name.maxLength &&
      //     errors.push("Name must be at most 10 characters long");
      //   !this.$v.name.required && errors.push("Name is required.");
      return errors;
    }
  }
};
</script>
