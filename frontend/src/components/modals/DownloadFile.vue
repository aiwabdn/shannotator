<template>
  <a-modal :id="id">
    <template v-slot:header>
      Download annotations as ...
    </template>

    <template v-slot:body>
      <h5 class="display-5">Choose an option</h5>
    </template>

    <template v-slot:footer>
      <button
        v-for="(name, idx) in supportedTypes"
        v-bind:key="idx"
        class="btn btn-info"
        data-dismiss="modal"
        @click="$emit('selected', name)"
      >
        {{ name }}
      </button>
    </template>
  </a-modal>
</template>

<script>
import aModal from "@/components/Modal.vue";

export default {
  name: "DownloadFile",

  components: {
    aModal
  },

  props: {
    id: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      supportedTypes: ["json", "yaml"]
    };
  }
};
</script>
