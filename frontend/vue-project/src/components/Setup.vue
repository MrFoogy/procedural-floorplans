<template>
  <div>
    <h1> Floor plan generator </h1>
    <div id="input">
      <v-text-field
        v-model="generations"
        label="Generations"
      ></v-text-field>
      <v-text-field
        v-model="individuals"
        label="Population size"
      ></v-text-field>
      <v-text-field
        v-model="building_size"
        label="Number of rooms"
      ></v-text-field>
      <v-text-field
        v-model="hof_size"
        label="Hall-of-fame size"
      ></v-text-field>
    </div>
    <v-btn color="accent" @click=fetchData> Run </v-btn>
  </div>
</template>

<script>  
import axios from 'axios'; 
export default {
  name: 'Setup',
  props: {
  },
  data: function() {
    return {
      generations: 10,
      individuals: 300,
      building_size: 9,
      hof_size: 10,
    }
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:5000/', {
        params: {
          generations: this.generations, 
          individuals: this.individuals, 
          building_size: this.building_size, 
          hof_size: this.hof_size, 
        }
      }).then(response => {
        this.$emit('dataFetched', response.data);
      });
      /*
      var data = [{x: 10, y: 20}, {x: 15, y: 10}];
      this.$emit('dataFetched', data);
      */
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  display: flex;
  align-items: center;
  flex-direction: column;
}
#input {
  flex-direction: row;
}
div * {
  padding: 20px;
}
</style>
