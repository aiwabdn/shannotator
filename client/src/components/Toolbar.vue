<template>
  <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
    <div class="btn-group mr-2" role="group" aria-label="Zoom group">
      <button type="button" class="btn btn-outline-primary" @click="$emit('zoomin')">
        Zoom in
      </button>
      <button type="button" class="btn btn-outline-primary" @click="$emit('zoomout')">
        Zoom out
      </button>
    </div>

    <div class="btn-group mr-2" role="group" aria-label="Navigation group">
      <button
        type="button"
        class="btn btn-outline-primary"
        :disabled="$store.state.currentFileIndex <= 0"
        @click="$emit('goprevious')"
      >
        Previous
      </button>
      <button
        type="button"
        class="btn btn-outline-primary"
        :disabled="$store.state.currentFileIndex === $store.getters.getNumFiles - 1"
        @click="$emit('gonext')"
      >
        Next
      </button>
    </div>

    <div class="btn-group mr-2" role="group" aria-label="Utility group">
      <button type="button" class="btn btn-outline-primary" @click="$emit('save')">Save</button>
      <button
        type="button"
        class="btn btn-outline-primary"
        data-toggle="modal"
        data-target="#downloadModal"
      >
        Download
      </button>

      <download-file id="downloadModal" @selected="$emit('download', $event)" />
    </div>

    <div class="btn-group mr-2" role="group" aria-label="Exit group">
      <button type="button" class="btn btn-outline-primary" @click="$emit('close')">
        Close Project
      </button>
    </div>
  </div>
</template>

<script>
import DownloadFile from "@/components/modals/DownloadFile.vue";

export default {
  name: "Toolbar",

  components: {
    DownloadFile
  },

  methods: {
    logclick(e) {
      console.log("client", e.clientX, e.clientY);
      console.log("page", e.pageX, e.pageY);
      console.log("scroll", e.scrollLeft, e.scrollTop);
    }
  }
};
</script>
