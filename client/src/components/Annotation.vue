<template>
  <div :style="positioning">
    <attribute-set type="selection" @change="setCurrentSelectionAttribute" />
  </div>
</template>

<script>
import AttributeSet from "@/components/AttributeSet.vue";

export default {
  name: "Annotation",

  components: {
    AttributeSet,
  },

  props: {
    left: {
      type: [Number, String],
      required: false,
    },
    top: {
      type: [Number, String],
      required: false,
    },
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
        maxWidth: "20%",
      },
    };
  },

  methods: {
    setCurrentSelectionAttribute(event) {
      this.$store.commit("setSelectionAttribute", event);
    },
  },
};
</script>
