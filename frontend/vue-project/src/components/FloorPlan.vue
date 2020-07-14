
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
      var lotWidth = Math.abs(data.lot.points[0][0] - data.lot.points[1][0]);
      var lotHeight = Math.abs(data.lot.points[1][1] - data.lot.points[2][1]);
      var scale = Math.min((this.canvasWidth - 50) / lotWidth, (this.canvasHeight - 50) / lotHeight);
      var extraX = this.canvasWidth - scale * lotWidth;
      var extraY = this.canvasHeight - scale * lotHeight;
      this.two.scene.translation.set(scale * (lotWidth / 2) + extraX / 2, scale * (lotHeight / 2) + extraY / 2);
      this.two.scene.scale = scale;
      this.createGrid(data.lot.points[0][0], data.lot.points[1][0], data.lot.points[1][1], data.lot.points[2][1], data.gridSize);
      var rect = this.two.makeRectangle(0.0, 0.0, 5.0, 5.0);
      rect.noFill();
      rect.linewidth = 0.1;
      rect.stroke = 'rgb(0, 200, 0)';
      this.two.update();
      for (var i = 0; i < data.rooms.length; i++) {
        this.createRoom(data.rooms[i]);
      }
      console.log(data);
    },
    createShape(shapeData, color) {
      var vertices = []
      for (var i = 0; i < shapeData.points.length; i++) {
        vertices.push(new Two.Anchor(shapeData.points[i][0], shapeData.points[i][1]));
        var circle = this.two.makeCircle(shapeData.points[i][0], shapeData.points[i][1], 0.15);
        circle.fill = 'rgb(150, 50, 50)';
        circle.opacity = 0.5;
        circle.linewidth = 0;
        /*
        var text = this.two.makeText(i, shapeData.points[i][0], shapeData.points[i][1])
        text.size = 0.8;
        */
        this.two.update();
      }
      var path = this.two.makePath(vertices, false);
      path.noFill();
      path.opacity = 1.0;
      path.stroke = color;
      path.linewidth = 0.1;
      this.two.update();
    },
    createRoom(roomData) {
      this.createShape(roomData.shape, 'rgb(0, 0, 0)');
      var text = this.two.makeText(roomData.name, roomData.shape.center[0], roomData.shape.center[1])
      text.size = 0.5;
      this.two.update();
    },
    createGrid(minX, maxX, minY, maxY, gridSize) {
      var minXDisc = this.discretizeLower(minX, gridSize);
      var maxXDisc = this.discretizeUpper(maxX, gridSize);
      var minYDisc = this.discretizeLower(minY, gridSize);
      var maxYDisc = this.discretizeUpper(maxY, gridSize);

      var current = minXDisc;
      var line;
      while (current <= maxXDisc) {
        line = this.two.makePath(current, minYDisc, current, maxYDisc, true);
        line.noFill;
        line.stroke = 'rgb(50, 50, 50)'
        line.linewidth = 0.02;
        line.opacity = 0.3;
        current += gridSize;
      }
      current = minYDisc;
      while (current <= maxXDisc) {
        line = this.two.makePath(minXDisc, current, maxXDisc, current, true);
        line.noFill;
        line.stroke = 'rgb(50, 50, 50)'
        line.linewidth = 0.02;
        line.opacity = 0.3;
        current += gridSize;
      }
      this.two.update();
    },
    discretizeLower(val, gridSize) {
      return Math.floor(val / gridSize) * gridSize;
    },
    discretizeUpper(val, gridSize) {
      return Math.ceil(val / gridSize) * gridSize;
    }
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
