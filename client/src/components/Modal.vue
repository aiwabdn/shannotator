<template>
  <div class="modal fade" :id="id" tabindex="-1" :aria-labelledby="`${id}Label`" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title mx-auto display-5" id="`${id}Label`">
            <slot name="header">
              Default Header
            </slot>
          </h5>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
            @click="$emit('close')"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div class="modal-body" style="overflow:auto">
          <slot name="body">
            Default Body
          </slot>
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button type="button" class="btn btn-info" data-dismiss="modal" @click="$emit('close')">
              Cancel
            </button>
            <button type="button" class="btn btn-info" data-dismiss="modal" @click="$emit('close')">
              OK
            </button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "aModal",

  props: {
    id: {
      type: String,
      required: true
    }
  }
};
</script>
