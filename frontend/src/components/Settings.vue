<template>
  <div class="container">
    <h5 class="display-5">
      Default Attributes
      <input
        type="button"
        class="btn btn-outline-secondary btn-sm pull-right"
        :value="editing ? 'Save' : 'Edit'"
        @click="editing = !editing"
      />
    </h5>
    <update-attribute id="modifyattributemodal" />

    <div id="default" v-for="(key, idx) in $store.getters.getAttributeNames()" v-bind:key="idx">
      <div v-if="isConditionMet(key) || editing">
        <attribute
          :id="`default-${key}`"
          :name="key"
          :inputType="$store.getters.getAttributeType(key)"
          :values="$store.getters.getAttributeValues(key)"
          :defaultValue="$store.getters.getDefaultValue(key)"
          :editable="editing"
          @change="setDefaultAttributeValue"
        />
      </div>
      <div v-else>
        {{ clearAttribute(key) }}
      </div>
    </div>
    <hr />

    <button
      v-if="editing"
      type="button"
      class="btn btn-info btn-sm w-100"
      data-toggle="modal"
      data-target="#modifyattributemodal"
    >
      Add
    </button>

    <div class="form-group">
      <label for="colour-attribute-selector">Region Colour</label>
      <select
        class="form-control"
        id="colour-attribute-selector"
        @change="coloringSelected($event)"
      >
        <option selected disabled>None</option>
        <option
          v-for="(name, idx) in $store.getters.getRadioAttributeNames()"
          v-bind:key="idx"
          :value="name"
          >{{ name }}</option
        >
      </select>
    </div>
  </div>
</template>

<script>
import UpdateAttribute from "@/components/modals/UpdateAttribute.vue";
import Attribute from "@/components/Attribute.vue";
import _ from "lodash";
import { CanvasManager } from "../utilities";

export default {
  name: "Settings",

  components: {
    UpdateAttribute,
    Attribute
  },

  data() {
    return {
      editing: false
    };
  },

  methods: {
    coloringSelected(event) {
      this.$store.commit("setColoringAttribute", event.target.value);
      CanvasManager.drawRegions();
    },

    setDefaultAttributeValue(event) {
      this.$store.commit("setDefaultAttribute", event);
    },

    isConditionMet(name) {
      const condition = this.$store.getters.getCondition(name);
      if (_.isEmpty(condition)) {
        return true;
      }

      let res = false;
      const [[k, v]] = _.toPairs(condition);
      const defaultValue = this.$store.getters.getDefaultValue(k);
      const attributeValues = this.$store.getters.getAttributeValues(k);
      switch (this.$store.getters.getAttributeType(k)) {
        case "radio":
          res = attributeValues.indexOf(v) === defaultValue;
          break;
        case "text":
          res = true;
          break;
        case "checkbox": {
          const valuesMapped = _.map(v, function f(o) {
            return attributeValues.indexOf(o);
          });
          res = _.isEqual(_.sortBy(valuesMapped), _.sortBy(defaultValue));
          // console.log("default checkbox valuesmapped", valuesMapped, defaultValue, res);
          break;
        }
        default:
          break;
      }
      return res;
    },

    clearAttribute(name) {
      this.$store.state.currentDefaults[name] = this.$store.getters.getIndeterminateValue(name);
    }
  }
};
</script>
