<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-btn color="accent" id="setupButton" @click="setupClick">
        Setup
      </v-btn>
      <v-tabs
        v-model="tab"
        optional
      >
        <v-tab
          v-for="item in items"
          :key="item.key"
        >
          {{ item.name }}
        </v-tab>
      </v-tabs>
    </v-app-bar>

    <v-content>
      <Setup v-if="tab == null" @dataFetched="addData"/>
      <Results v-else :fullData="selectedData"/>
    </v-content>
  </v-app>
</template>

<script>
import Setup from './components/Setup';
import Results from './components/Results';

export default {
  name: 'App',

  components: {
    Setup,
    Results,
  },

  data: function() {
    return {
      tab: null,
      items: [
      ]
    }
  },

  computed: {
    selectedData: function() {
      return this.items[this.tab].data;
    },
  },

  methods: {
    setupClick : function() {
      this.tab = null;
    },
    addData: function(newData) {
      var newItemNum = this.items.length;
      this.items.push({ key: "Tab" + newItemNum, name: "Data " + newItemNum, data: newData})
    },
  },
};
</script>

<style>
#setupButton {
  margin-right: 20px;
}
</style>