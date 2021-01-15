<template>
  <fieldset :id="id">
    <legend>
      {{ name }}
      <input
        v-if="editable"
        type="button"
        class="btn btn-outline-secondary btn-sm pull-right"
        value="Edit"
        data-toggle="modal"
        :data-target="`#${name}-editattributemodal`"
      />
    </legend>

    <div v-if="inputType === 'radio' || inputType === 'checkbox'">
      <div class="form-check form-check-inline" v-for="(value, index) in values" v-bind:key="index">
        <label class="form-check-label" :for="`${id}${index}`">
          <input
            :id="`${id}${index}`"
            :type="inputType"
            class="form-check-input"
            :value="index"
            :checked="isDefault(index)"
            @change="modified(index)"
          />
          {{ value }}
        </label>
      </div>
    </div>

    <div v-if="inputType === 'text'" class="container-fluid">
      <input
        :id="`${id}${name}`"
        :type="inputType"
        class="form-control form-control-sm"
        :value="defaultValue"
        placeholder="Default Text is empty"
        @input="modified($event.target.value)"
        @focusin="$store.commit('toggleEditing')"
        @focusout="$store.commit('toggleEditing')"
      />
    </div>

    <update-attribute :id="`${name}-editattributemodal`" :initial="name" />
  </fieldset>
</template>

<script>
import UpdateAttribute from "@/components/modals/UpdateAttribute.vue";

export default {
  name: "Attribute",

  components: {
    UpdateAttribute
  },

  emits: ["change"],

  props: {
    id: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    inputType: {
      type: String,
      required: true
    },
    values: {
      type: [String, Array],
      required: true
    },
    defaultValue: {
      type: [Number, String, Array],
      required: false
    },
    editable: {
      type: Boolean,
      default: false,
      required: false
    }
  },

  methods: {
    modified(option) {
      this.$emit("change", { key: this.name, value: option });
    },
    isDefault(option) {
      // console.log("checking for", this.name, this.defaultValue, option);
      let res;
      switch (this.inputType) {
        case "radio":
          res = option === this.defaultValue;
          break;
        case "checkbox":
          res = this.defaultValue.indexOf(option) > -1;
          break;
        default:
          break;
      }
      return res;
    }
  }
};
</script>

<style>
legend {
  background-color: #ccf7e2;
  color: #000000;
  padding: 3px 6px;
  font-size: 12px;
}

.output {
  font: 1rem "Fira Sans", sans-serif;
}

input {
  margin: 0.4rem;
}
</style>
