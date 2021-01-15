<template>
  <div :style="positioning">
    <h5 class="display-5">Selection Attributes</h5>
    <div v-for="(key, idx) in $store.getters.getAttributeNames()" v-bind:key="idx">
      <div v-if="isConditionMet(key)">
        <attribute
          :id="`selection-${key}`"
          :name="key"
          :inputType="$store.getters.getAttributeType(key)"
          :values="$store.getters.getAttributeValues(key)"
          :defaultValue="$store.getters.getSelectionValue(key)"
          @change="setCurrentSelectionAttribute"
        />
      </div>
      <div v-else>
        {{ clearAttribute(key) }}
      </div>
    </div>
  </div>
</template>

<script>
import Attribute from "@/components/Attribute.vue";
import _ from "lodash";

export default {
  name: "Annotation",
  components: {
    Attribute
  },

  props: {
    left: {
      type: [Number, String],
      required: false
    },
    top: {
      type: [Number, String],
      required: false
    }
  },

  data() {
    return {
      positioning: {
        position: "absolute",
        display: "block",
        background: "white",
        zIndex: "100",
        left: `${this.left}px`,
        top: `${this.top}px`,
        border: "black solid 2px",
        padding: "3px",
        borderRadius: "5px",
        width: "20%",
        maxWidth: "20%"
      }
    };
  },

  methods: {
    setCurrentSelectionAttribute(event) {
      this.$store.commit("setSelectionAttribute", event);
    },

    isConditionMet(name) {
      const condition = this.$store.getters.getCondition(name);
      if (_.isEmpty(condition)) {
        return true;
      }

      let res = false;
      const [[k, v]] = _.toPairs(condition);
      const selectionValue = this.$store.getters.getSelectionValue(k);
      const attributeValues = this.$store.getters.getAttributeValues(k);
      switch (this.$store.getters.getAttributeType(k)) {
        case "radio":
          res = attributeValues.indexOf(v) === selectionValue;
          break;
        case "text":
          res = true;
          break;
        case "checkbox": {
          const valuesMapped = _.map(v, function f(o) {
            return attributeValues.indexOf(o);
          });
          res = _.isEqual(_.sortBy(valuesMapped), _.sortBy(selectionValue));
          break;
        }
        default:
          break;
      }
      return res;
    },

    clearAttribute(name) {
      this.$store.state.currentAnnotations.regions[
        this.$store.state.currentSelectionIndex
      ].attributes[name] = this.$store.getters.getIndeterminateValue(name);
    }
  }
};
</script>
