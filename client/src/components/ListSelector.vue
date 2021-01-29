<template>
  <v-card d-flex>
    <v-list>
      <v-list-item-group :value="monitor" active-class="border" color="indigo">
        <v-list-item
          v-for="(item, idx) in items"
          :key="idx"
          @click="$emit('selected', idx)"
        >
          <v-list-item-content>
            {{ item }}
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: "ListSelector",

  props: {
    items: {
      type: Array,
      required: true
    },
    monitor: {
      type: Number,
      required: false,
      default: -1
    }
  }
};
</script>
