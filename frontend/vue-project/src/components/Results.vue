<template>
  <div id="top">
    <div id="building">
      <v-pagination
        v-model="resultId"
        :length="numResults"
        :total-visible="10"
      ></v-pagination>
      <div id="scores">
        <li class="scoreText" v-for="(value, score_type) in resultScores" :key="score_type" solo :value="score_type + ' : ' + value" readonly dense rounded 
          full-width=false>
          {{ score_type }} : {{ value }}
        </li>
      </div>
      <div id="mynetwork"></div>
    </div>
    <div id="graphs">
      <p> {{ activeData }} </p>
      <canvas id="chart" width="600" height="350"> </canvas>
      <v-radio-group v-model="selectedStat" row>
        <v-radio v-for="stat in stats" :key="stat" :label="stat" :value="stat"></v-radio>
      </v-radio-group>
    </div>
  </div>
</template>

<script>  
import Chart from 'chart.js'
import { DataSet } from "vis-data/peer";
import { Network } from "vis-network/peer";
import "vis-network/styles/vis-network.css";

export default {
  name: 'Results',
  props: ['fullData'],
  data: function() {
    return {
      chart: null,
      selectedStat: null,
      resultId: 1,
      numResults: 0,
      resultScores: [],
      activeData: null,
      stats: null,
    }
  },
  mounted() {
    // create a network

    Chart.defaults.global.elements.point.radius = 3;
    Chart.defaults.global.elements.point.hitRadius = 3;
    Chart.defaults.global.elements.point.hoverRadius = 4;
    Chart.defaults.global.elements.point.borderColor = "black";
    Chart.defaults.global.elements.point.borderWidth = 1;
    this.chart = new Chart('chart', {
      type: 'line',
      data: null,
      options: {
        scales: {
          xAxes: [{
            position: 'bottom',
            type: "linear",
            scaleLabel: {
              display: true,
              labelString: "generation",
            },
          }]
        },
        responsive: false,
        animation: false,
      }
    });
    this.updateChart();
    this.updateNetwork();
  },
  methods: {
    updateChart() {
      if (this.chart == null) return;
      if (this.stats == null) {
        this.stats = this.fullData["graph"]["titles"];
      }
      if (this.selectedStat == null || !this.stats.includes(this.selectedStat)) {
        this.selectedStat = this.fullData["graph"]["titles"][0];
      }
      this.updateChartData();
      this.chart.update();
    },

    updateChartData() {
      if (this.chart.data.datasets.length == 0) {
        var newData = { datasets: []};
        var colors = ['rgba(100,100,200,1.0)', 'rgba(100,200,100,1.0)', 'rgba(200,100,100,1.0)'];
        for (let [index, label] of Object.keys(this.fullData["graph"]["data"][this.selectedStat]).entries()) {
          var dataSet = {label: label,  borderColor: colors[index], pointBorderColor: "white", pointBackgroundColor: colors[index], fill: false, lineTension: 0.0, data: []}
          newData["datasets"].push(dataSet);
        }
        this.chart.data = newData;
      }
      for (var i = 0; i < this.chart.data.datasets.length; i++) {
        var element = this.chart.data.datasets[i];
        var sourceData = this.fullData["graph"]["data"][this.selectedStat][element.label];
        element.data = [];
        for (var j = 0; j < sourceData.length; j++) {
          element.data.push({x: j, y: sourceData[j]});
        }
      }
    },

    updateNetwork() {
      this.numResults = this.fullData["hof"].length;
      this.resultScores = this.fullData["hof"][this.resultId - 1]["scores"];
      var nodes_data = this.fullData["hof"][this.resultId - 1]["nodes"];
      var edges = new DataSet(this.fullData["hof"][this.resultId - 1]["edges"]);
      for (var i = 0; i < nodes_data.length; i++) {
        nodes_data[i]["color"] = nodes_data[i]["exterior_connected"] ? 'rgba(255,200,200,1.0)' : 'rgba(200,200,255,1.0)';
      }
      var nodes = new DataSet(nodes_data);
      var networkContainer = document.getElementById("mynetwork");
      var networkData = {
        nodes: nodes,
        edges: edges,
      };
      var networkOptions = {    
        nodes: {
          shadow: {
            enabled: true,
            color: 'rgba(0,0,0,0.5)',
            size:4,
            x:4,
            y:4
          },
        },
      };
      console.log("Init network!");
      new Network(networkContainer, networkData, networkOptions);
      console.log("Should update network!");
    },
  },
  watch: {
    fullData: function() {
      this.updateChart();
      this.updateNetwork();
    },
    selectedStat: function() {
      this.updateChart();
    },
    resultId: function() {
      this.updateNetwork();
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
#top {
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
}
#scores {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  width: 500px;
  height: auto;
}
div * {
  padding: 10px;
}
#mynetwork {
  width: 600px;
  height: 450px;
  border: 1px solid lightgray;
}
.scoreText {
  width: auto;
}
</style>
