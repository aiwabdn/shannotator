<template>
  <v-container>
    <h2 class="ma-3">
      Default Attributes
      <v-btn icon right x-small type="button" @click="editing = !editing"
        ><v-icon>mdi-pencil</v-icon>
      </v-btn>
    </h2>
    <div
      v-for="(key, idx) in $store.getters.getAttributeNames()"
      v-bind:key="idx"
    >
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
  </v-container>
</template>

<script>
import Attribute from "@/components/Attribute.vue";
import _ from "lodash";
import { CanvasManager } from "../utilities";

export default {
  name: "DefaultAttributes",

  components: {
    Attribute,
  },

  data() {
    return {
      editing: false,
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
      this.$store.state.currentDefaults[
        name
      ] = this.$store.getters.getIndeterminateValue(name);
    },
  },
};
</script>