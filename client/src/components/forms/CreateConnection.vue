<template>
  <v-row justify="center">
    <v-dialog v-model="showing" width="30%" max-width="50%">
      <v-card>
        <v-card-title>Create New Connection</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              outlined
              dense
              v-model="name"
              :error-messages="nameErrors"
              label="Name"
              required
            ></v-text-field>
            <v-select
              outlined
              dense
              v-model="storageType"
              :items="Object.keys(supportedStorages)"
              :error-messages="selectErrors"
              label="Storage Type"
              required
              @change="showParams = true"
            ></v-select>
            <div v-if="showParams">
              <div
                v-for="(param, index) in supportedStorages[storageType]"
                v-bind:key="index"
                class="form-group"
              >
                <v-text-field
                  outlined
                  dense
                  :label="param.name"
                  :id="`${param.name}field`"
                  :placeholder="param.description"
                  required
                  @change="setParam(param.name, $event)"
                />
              </div>
            </div>
          </v-form>
        </v-card-text>
        <v-divider class="mt-12"></v-divider>
        <v-card-actions>
          <v-btn color="red lighten-4" @click="showing = false"> Cancel </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="teal lighten-4" @click="saveConnection"> Submit </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import { SERVER_ADDR } from "../../utilities";

export default {
  name: "CreateConnection",

  props: {
    flag: {
      type: Boolean,
      required: true
    }
  },

  data() {
    return {
      name: "",
      storageType: "",
      supportedStorages: {
        Local: []
      },
      showParams: false,
      parameters: {}
      //   showing: this.flag,
    };
  },

  validations: {
    name: {
      required
    },
    storageType: {
      required
    }
  },

  methods: {
    saveConnection() {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          name: this.name,
          storage_type: this.storageType,
          params: this.parameters
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      fetch(`${SERVER_ADDR}/create_connection`, requestOptions).catch(e => {
        console.log(e);
        return e;
      });
      this.showing = false;
    },

    createStorageParams() {
      this.supportedStorages[this.storageType].forEach(item => {
        this.parameters[item.name] = "";
      });
      console.log(this.parameters);
    },
    setParam(key, value) {
      this.parameters[key] = value;
      console.log(this.parameters);
    }
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
    },
    nameErrors() {
      const errors = [];
      //   if (!this.$v.name.$dirty) return errors;
      //   !this.$v.name.maxLength &&
      //     errors.push("Name must be at most 10 characters long");
      //   !this.$v.name.required && errors.push("Name is required.");
      return errors;
    }
  },

  mounted() {
    const requestOptions = {
      method: "GET"
    };

    fetch(`${SERVER_ADDR}/supported_storages`, requestOptions)
      .then(response => response.json())
      .then(data => (this.supportedStorages = data.storage_types))
      .catch(e => {
        console.log(e);
        return e;
      });
  }
};
</script>
