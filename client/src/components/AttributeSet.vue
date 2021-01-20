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
            :type="type"
            :inputType="$store.getters.getAttributeType(key)"
            :values="$store.getters.getAttributeValues(key)"
            :defaultValue="getValue(key)"
            :editable="editing"
            @change="$emit('change', $event)"
            @delete="deleteAttribute(key)"
          />
        </div>
      </template>
    </v-card-text>
  </v-card>
</template>

<script>
import Attribute from "@/components/Attribute.vue";
import { saveAttributes } from "../utilities";

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

    deleteAttribute(name) {
      this.$store.commit("deleteAttribute", name);
      this.forceRerender();
      saveAttributes();
    },
  },
};
</script>