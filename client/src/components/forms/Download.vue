<template>
  <!-- <v-row justify="center"> -->
  <v-dialog v-model="showing" width="30%" max-width="50%">
    <v-card>
      <v-card-text>
        <v-card-title>Download Annotations</v-card-title>
        <!-- <v-form> -->
        <v-select
          outlined
          dense
          v-model="chosenType"
          :items="supportedFileTypes"
          label="Annotation format"
          placeholder="Select a format for downloading"
          required
        ></v-select>
        <!-- </v-form> -->
      </v-card-text>
      <v-divider class="mt-12"></v-divider>
      <v-card-actions>
        <v-btn text @click="showing = false"> Cancel </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="teal lighten-2" text @click="chosenFormat()">
          Download
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <!-- </v-row> -->
</template>

<script>
export default {
  name: "Download",

  props: {
    flag: {
      type: Boolean,
      required: true
    }
  },

  data() {
    return {
      chosenType: "",
      supportedFileTypes: ["json", "yaml"]
    };
  },

  methods: {
    chosenFormat() {
      this.$emit("selected", this.chosenType);
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
    }
  }
};
</script>
