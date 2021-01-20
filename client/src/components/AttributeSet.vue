<template>
  <v-card rounded="true" outlined :key="refreshCounter">
    <v-card-text>
      <template>
        <div
          v-for="(key, idx) in $store.getters.getAttributeNames()"
          v-bind:key="idx"
        >
          <attribute
            :id="`${type}-${key}`"
            :name="key"
            :inputType="$store.getters.getAttributeType(key)"
            :values="$store.getters.getAttributeValues(key)"
            :defaultValue="getValue(key)"
            :editable="editing"
            :disabled="!(isConditionMet(key) || editing)"
            @change="$emit('change', $event)"
            @delete="deleteAttribute(key)"
          />
          <!-- <div v-if="isConditionMet(key) || editing">Hello</div>
          <div v-else>
            {{ clearAttribute(key) }}
          </div> -->
        </div>
      </template>
    </v-card-text>
  </v-card>
</template>

<script>
import Attribute from "@/components/Attribute.vue";
import { saveAttributes } from "../utilities";
import _ from "lodash";

export default {
  name: "AttributeSet",

  props: {
    editing: {
      type: Boolean,
      required: false,
      default: false,
    },
    type: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      refreshCounter: 0,
    };
  },

  components: {
    Attribute,
  },

  methods: {
    forceRerender() {
      this.refreshCounter += 1;
      // console.log("refreshed to", this.refreshCounter);
    },

    getValue(key) {
      switch (this.type) {
        case "default":
          return this.$store.getters.getDefaultValue(key);
        case "selection":
          return this.$store.getters.getSelectionValue(key);
        default:
          break;
      }
    },

    isConditionMet(name) {
      const condition = this.$store.getters.getCondition(name);
      if (_.isEmpty(condition)) {
        return true;
      }

      let res = false;
      const [[k, v]] = _.toPairs(condition);
      const currentValue = this.getValue(k);
      const attributeValues = this.$store.getters.getAttributeValues(k);
      switch (this.$store.getters.getAttributeType(k)) {
        case "radio":
          res = attributeValues.indexOf(v) === currentValue;
          break;
        case "text":
          res = true;
          break;
        case "checkbox": {
          const valuesMapped = _.map(v, function f(o) {
            return attributeValues.indexOf(o);
          });
          res = _.isEqual(_.sortBy(valuesMapped), _.sortBy(currentValue));
          // console.log("default checkbox valuesmapped", valuesMapped, currentValue, res);
          break;
        }
        default:
          break;
      }
      //   console.log("condition for", name, res);
      return res;
    },

    clearAttribute(name) {
      switch (this.type) {
        case "default": {
          this.$store.state.currentDefaults[
            name
          ] = this.$store.getters.getIndeterminateValue(name);
          break;
        }
        case "selection": {
          this.$store.state.currentAnnotations.regions[
            this.$store.state.currentSelectionIndex
          ].attributes[name] = this.$store.getters.getIndeterminateValue(name);
          break;
        }
        default:
          break;
      }
    },

    deleteAttribute(name) {
      this.$store.commit("deleteAttribute", name);
      this.forceRerender();
      saveAttributes();
    },
  },
};
</script>