<template>
  <!-- <div id="app">
    <bar />
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
  </div> -->
  <v-app id="app">
    <bar />
    <v-main>
      <v-container fluid fill-height>
        <!-- fill-height style="border: solid black 2px"> -->
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Bar from "@/components/Bar.vue";

export default {
  components: {
    Bar
  }
};
</script>
<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: Roboto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #ccf7e2; */
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
