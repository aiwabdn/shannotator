<template>
  <a-modal :id="id">
    <template v-slot:header>
      <div v-if="initial.length > 0">
        Edit attribute
      </div>
      <div v-else-if="initial.length === 0">
        Add attribute
      </div>
    </template>

    <template v-slot:body>
      <div class="form">
        <div class="form-group">
          <label for="attribute-name">Name</label>
          <input
            :id="`${id}-attribute-name`"
            type="text"
            class="form-control"
            v-model.trim="attributeName"
            placeholder="attribute name"
            aria-label="addname"
            aria-describedby="addname"
            required
          />
        </div>

        <div class="form-group">
          <label for="possible-input-types">Type</label>
          <div id="possible-input-types" class="form-control">
            <div
              class="form-check form-check-inline"
              v-for="(value, index) in possibleInputTypes"
              v-bind:key="index"
            >
              <label class="form-check-label" :for="`datatype${index}`">
                <input
                  :id="`datatype${index}`"
                  type="radio"
                  class="form-check-input"
                  :value="value"
                  v-model="attributeType"
                  required
                />
                {{ value }}
              </label>
            </div>
          </div>
        </div>

        <div class="form-group" v-if="attributeType === 'radio' || attributeType === 'checkbox'">
          <label for="attribute-values">Values</label>
          <input
            :id="`${id}-attribute-values`"
            type="text"
            class="form-control"
            v-model="attributeValues"
            placeholder="values: ',' separated"
            aria-label="addvalues"
            aria-describedby="addvalues"
            @focusin="$store.commit('toggleEditing')"
            @focusout="$store.commit('toggleEditing')"
            required
          />
        </div>

        <div class="form-group">
          <label for="conditionSelector">Condition</label>
          <select class="form-control" id="conditionSelector" v-model="conditionName">
            <option selected disabled value="">Choose one...</option>
            <option
              v-for="(name, idx) in $store.getters.getAttributeNames()"
              v-bind:key="idx"
              :value="name"
              >{{ name }}</option
            >
          </select>
        </div>

        <div v-if="conditionName.length > 0">
          <div
            class="form-group"
            v-if="['radio', 'checkbox'].includes($store.getters.getAttributeType(conditionName))"
          >
            <legend for="condition-values">Select condition value for "{{ conditionName }}"</legend>
            <div
              id="condition-values"
              class="form-check form-check-inline"
              v-for="(value, index) in $store.getters.getAttributeValues(conditionName)"
              v-bind:key="index"
            >
              <label class="form-check-label" :for="`condition${id}${index}`">
                <input
                  :id="`condition${id}${index}`"
                  :type="$store.getters.getAttributeType(conditionName)"
                  class="form-check-input"
                  :value="value"
                  @change="setConditionValue(value)"
                />
                {{ value }}
              </label>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template v-slot:footer>
      <button class="btn btn-outline-secondary" data-dismiss="modal" @click="$emit('close')">
        Cancel
      </button>
      <button class="btn btn-outline-primary" data-dismiss="modal" @click="updateAttribute">
        Save
      </button>
    </template>
  </a-modal>
</template>

<script>
import aModal from "@/components/Modal.vue";
import _ from "lodash";

export default {
  name: "UpdateAttribute",

  components: {
    aModal
  },

  props: {
    id: {
      type: String,
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
      conditionValue: ""
    };
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

    updateAttribute() {
      if (this.attributeName === "") {
        console.log("provide a name for the attribute");
        return;
      }
      const update = {
        name: this.attributeName,
        type: this.attributeType,
        values: this.attributeType === "text" ? "" : this.attributeValues.split(","),
        condition: this.getParsedCondition()
      };
      this.$store.commit("updateAttribute", update);
      this.saveAttributes();
      this.$emit("close");
    },

    getParsedCondition() {
      const condition = {};
      if (this.conditionName.length > 0) {
        condition[this.conditionName] = this.conditionValue;
      }
      return condition;
    },

    saveAttributes() {
      const requestOptions = {
        method: "POST",
        body: JSON.stringify({
          project: this.$store.state.projectName,
          attributes: this.$store.state.projectSettings.attributes
        }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      };
      fetch("http://localhost:8000/update_attributes", requestOptions);
    }
  },

  created() {
    if (this.initial.length > 0) {
      this.attributeName = this.initial;
      // console.log("getting attrib type", this.initial);
      this.attributeType = this.$store.getters.getAttributeType(this.initial);
      this.attributeValues = this.$store.getters.getAttributeValues(this.initial);
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
      if (this.conditionName.length > 0) {
        return this.$store.getters.getAttributeType(this.conditionName);
      }
      return "";
    }
  }
};
</script>
