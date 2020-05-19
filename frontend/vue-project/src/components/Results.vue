<template>
  <div>
    <h1> Results </h1>
    <p> {{ data }} </p>
  </div>
</template>

<script>  
export default {
  name: 'Results',
  props: ['data'],
  data: function() {
    return {
    }
  },
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
