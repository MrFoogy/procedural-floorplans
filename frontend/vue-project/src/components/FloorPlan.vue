
<template>
  <div>
    <div id="two-container"/>
  </div>
</template>

<script>  
import Two from 'two.js'
export default {
  name: 'FloorPlan',
  props: {
  },
  data: function() {
    return {
      two: null,
      canvasWidth: 600,
      canvasHeight: 600,
    }
  },
  methods: {
    setData(data) {
      this.createShape(data.lot, 'rgb(50, 50, 50)');
      var lotWidth = data.lot.width;
      var lotHeight = data.lot.height;
      var scale = Math.min((this.canvasWidth - 50) / lotWidth, (this.canvasHeight - 50) / lotHeight);
      var extraX = this.canvasWidth - scale * lotWidth;
      var extraY = this.canvasHeight - scale * lotHeight;
      this.two.scene.translation.set(scale * (lotWidth / 2) + extraX / 2, scale * (lotHeight / 2) + extraY / 2);
      this.two.scene.scale = scale;
      for (var i = 0; i < data.rooms.length; i++) {
        this.createRoom(data.rooms[i]);
      }
      console.log(data);
    },
    createShape(shapeData, color) {
      var height = shapeData.height;
      var width = shapeData.width;
      var position = shapeData.position;
      var rect = this.two.makeRectangle(position[0], position[1], width, height);
      rect.noFill();
      rect.opacity = 1.0;
      rect.stroke = color;
      rect.linewidth = 0.1;
      this.two.update();
    },
    createRoom(roomData) {
      this.createShape(roomData.shape, 'rgb(0, 0, 0)');
      var text = this.two.makeText(roomData.name, roomData.shape.position[0], roomData.shape.position[1])
      text.size = 0.5;
      this.two.update();
    },
  },
  mounted() {
    // Make an instance of two and place it on the page.
    var elem = document.getElementById('two-container');
    var params = { width: this.canvasWidth, height: this.canvasHeight };
    this.two = new Two(params).appendTo(elem);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#two-container {
  background-color: wheat;
  padding: 0;
  margin: 0;
}
</style>
