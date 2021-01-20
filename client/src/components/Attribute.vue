<template>
  <div class="ma-2">
    <v-row class="justify-space-around">
      <span class="legend">
        {{ name }}
        <div
          style="float: right"
          v-bind:style="{ visibility: editable ? 'visible' : 'hidden' }"
        >
          <v-btn icon x-small type="button" @click="editing = true"
            ><v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon x-small type="button" @click="$emit('delete')"
            ><v-icon>mdi-delete</v-icon>
          </v-btn>
        </div>
      </span>
    </v-row>

    <v-row class="justify-space-around" v-if="inputType === 'checkbox'">
      <v-checkbox
        v-model="modelValue"
        v-for="(value, idx) in values"
        v-bind:key="idx"
        :value="idx"
        :success="isDefault(idx)"
        :label="value"
        :disabled="disabled"
        @change="modified(idx)"
      ></v-checkbox>
    </v-row>

    <v-row class="justify-space-around" v-if="inputType === 'radio'">
      <v-radio-group row v-model="modelValue">
        <v-radio
          v-for="(value, idx) in values"
          v-bind:key="idx"
          :value="idx"
          :success="isDefault(idx)"
          :label="value"
          :disabled="disabled"
          @change="modified(idx)"
        ></v-radio>
      </v-radio-group>
    </v-row>

    <v-row class="justify-space-around" v-if="inputType === 'text'">
      <v-text-field
        dense
        full-width
        clearable
        :value="defaultValue"
        placeholder="Default Text is empty"
        :disabled="disabled"
        @input="modified($event)"
        @focusin="$store.commit('toggleEditing')"
        @focusout="$store.commit('toggleEditing')"
      />
    </v-row>
    <update-attribute
      :flag="editing"
      :initial="name"
      @click:outside="editing = false"
      @close="editing = false"
    />
  </div>
</template>

<script>
import UpdateAttribute from "./forms/UpdateAttribute.vue";
export default {
  name: "Attribute",

  components: { UpdateAttribute },

  emits: ["change"],

  data() {
    return {
      editing: false,
    };
  },

  props: {
    id: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    inputType: {
      type: String,
      required: true,
    },
    values: {
      type: [String, Array],
      required: true,
    },
    defaultValue: {
      type: [Number, String, Array],
      required: false,
    },
    editable: {
      type: Boolean,
      default: false,
      required: false,
    },
    disabled: {
      type: Boolean,
      default: false,
      required: false,
    },
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
          res = option === this.modelValue;
          break;
        case "checkbox":
          //   res = this.defaultValue.indexOf(option) > -1;
          res = this.modelValue.includes(option);
          break;
        default:
          break;
      }
      return res;
    },
  },

  computed: {
    modelValue: {
      get: function () {
        return this.defaultValue;
      },
      set: function () {
        // do nothing here as we are emitting the changes
        return;
      },
    },
  },
};
</script>

<style>
.legend {
  background-color: #ccf7e2;
  width: 100%;
}
</style>
