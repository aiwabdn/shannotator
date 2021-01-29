<template>
  <v-row justify="center">
    <v-dialog v-model="showing" width="30%" max-width="50%">
      <v-card>
        <v-card-title>Update Attribute</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              outlined
              dense
              v-model.trim="attributeName"
              :error-messages="nameErrors"
              label="Name"
              placeholder="Name the attribute"
              required
            ></v-text-field>
            <v-select
              outlined
              dense
              v-model="attributeType"
              :items="possibleInputTypes"
              :error-messages="selectErrors"
              label="Type"
              placeholder="Choose a type for the attribute"
              required
            ></v-select>
            <v-text-field
              outlined
              dense
              v-if="attributeType === 'radio' || attributeType === 'checkbox'"
              v-model.trim="attributeValues"
              :error-messages="valuesErrors"
              label="Values"
              placeholder="Enter ',' separated values"
              required
            ></v-text-field>
            <v-select
              outlined
              dense
              clearable
              v-model="conditionName"
              :items="$store.getters.getAttributeNames()"
              :error-messages="conditionNameErrors"
              label="Condition"
              placeholder="Select an attribute to condition on"
              required
              @change="setDefaultConditionValue()"
            ></v-select>

            <div
              v-bind:style="{
                visibility:
                  conditionName && conditionName.length > 0
                    ? 'visible'
                    : 'hidden'
              }"
            >
              <span>Select conditional value for {{ conditionName }}</span>
              <v-row
                class="justify-space-around"
                v-if="conditionType === 'checkbox'"
              >
                <v-checkbox
                  v-model="conditionValue"
                  v-for="(value, idx) in $store.getters.getAttributeValues(
                    conditionName
                  )"
                  v-bind:key="idx"
                  :value="idx"
                  :label="value"
                ></v-checkbox>
              </v-row>

              <v-row
                class="justify-space-around"
                v-if="conditionType === 'radio'"
              >
                <v-radio-group row v-model="conditionValue">
                  <v-radio
                    v-for="(value, idx) in $store.getters.getAttributeValues(
                      conditionName
                    )"
                    v-bind:key="idx"
                    :value="idx"
                    :label="value"
                  ></v-radio>
                </v-radio-group>
              </v-row>
            </div>
          </v-form>
        </v-card-text>
        <v-divider class="mt-12"></v-divider>
        <v-card-actions>
          <v-btn color="red lighten-4" @click="showing = false"> Cancel </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="teal lighten-4" @click="updateAttribute()">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import { saveAttributes } from "../../utilities";
import _ from "lodash";

export default {
  name: "UpdateAttribute",

  components: {},

  props: {
    flag: {
      type: Boolean,
      required: true
    },

    initial: {
      type: String,
      default: ""
    }
  },

  data() {
    return {
      possibleInputTypes: ["radio", "checkbox", "text"],
      attributeName: "",
      attributeType: "",
      attributeValues: "",
      conditionName: "",
      conditionValue: "",
      modelValue: ""
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
    setConditionValue(value) {
      switch (this.conditionType) {
        case "radio":
          this.conditionValue = value;
          break;
        case "checkbox": {
          if (typeof this.conditionValue === "string") {
            this.conditionValue = [];
          }
          const idx = this.conditionValue.indexOf(value);
          if (idx > -1) {
            this.conditionValue.slice(idx, 1);
          } else {
            this.conditionValue.push(value);
          }
          break;
        }
        case "text":
          this.conditionValue = "";
          break;
        default:
          break;
      }
    },

    setDefaultConditionValue() {
      if (this.initial.length === 0) {
        if (
          this.$store.getters.getAttributeType(this.conditionName) ===
          "checkbox"
        ) {
          this.conditionValue = [];
          console.log("checkbox type", this.conditionValue);
        }
      }
    },

    updateAttribute() {
      if (this.attributeName === "") {
        console.log("provide a name for the attribute");
        return;
      }
      const update = {
        name: this.attributeName,
        type: this.attributeType,
        values:
          this.attributeType === "text" ? "" : this.attributeValues.split(","),
        condition: this.getParsedCondition()
      };
      this.$store.commit("updateAttribute", update);
      saveAttributes();
      this.showing = false;
    },

    getParsedCondition() {
      const condition = {};
      if (this.conditionName && this.conditionName.length > 0) {
        condition[this.conditionName] = this.conditionValue;
      }
      return condition;
    }
  },

  mounted() {
    if (this.initial.length > 0) {
      this.attributeName = this.initial;
      // console.log("getting attrib type", this.initial);
      this.attributeType = this.$store.getters.getAttributeType(this.initial);
      this.attributeValues = this.$store.getters.getAttributeValues(
        this.initial
      );
      if (this.attributeType !== "text") {
        this.attributeValues = this.attributeValues.join(",");
      }
      const condition = this.$store.getters.getCondition(this.initial);
      // TODO: make this better. It is cringeworthy right now
      if (!_.isEmpty(condition)) {
        [[this.conditionName, this.conditionValue]] = Object.entries(condition);
      }
    }
  },

  computed: {
    conditionType() {
      if (this.conditionName && this.conditionName.length > 0) {
        return this.$store.getters.getAttributeType(this.conditionName);
      }
      return "";
    },
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
      return errors;
    },
    nameErrors() {
      const errors = [];
      return errors;
    },
    valuesErrors() {
      const errors = [];
      return errors;
    },
    conditionNameErrors() {
      const errors = [];
      return errors;
    }
  }
};
</script>
