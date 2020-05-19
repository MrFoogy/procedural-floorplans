<template>
  <div>
    <h1> Floor plan generator </h1>
    <v-btn @click=fetchData id="donald"> Run algorithm </v-btn>
    <p> {{ serverText }} </p>
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
      serverText: "",
    }
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:5000/').then(response => {
        this.$emit('dataFetched', response.data);
      });
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
div * {
  padding: 20px;
}
</style>
