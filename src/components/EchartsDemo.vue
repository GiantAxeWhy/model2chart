<template>
  <div>
    <div class="chart-container">
      <!-- <div ref="barChart" class="chart"></div>
      <div ref="lineChart" class="chart"></div>
      <div ref="pieChart" class="chart"></div> -->
      <ChartWrapper :chartData="chartData" chartType="bar" class="chart" />
      <ChartWrapper :chartData="chartData" chartType="line" class="chart" />
      <ChartWrapper :chartData="chartData" chartType="pie" class="chart" />
      <!-- <div ref="tableChart" class="chart">
        <table v-if="chartData">
          <thead>
            <tr>
              <th>月份</th>
              <th>负面反馈数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, index) in chartData.xAxis" :key="index">
              <td>{{ value }}</td>
              <td>{{ chartData.yAxis[index] }}</td>
            </tr>
          </tbody>
        </table>
      </div> -->
      <div class="chart">
        <table v-if="chartData && chartData.xAxis && chartData.yAxis">
          <thead>
            <tr>
              <th>月份</th>
              <th>负面反馈数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, index) in chartData.xAxis" :key="index">
              <td>{{ value }}</td>
              <td>{{ chartData.yAxis[index] }}</td>
            </tr>
          </tbody>
        </table>
        <div v-else class="no-data">暂无数据</div>
      </div>
    </div>

    <input
      style="margin-top: 14%"
      v-model="inputText"
      @keyup.enter="sendRequest"
      placeholder="输入额外要求并按回车"
    />
  </div>
</template>

<script>
// import * as echarts from "echarts";
import axios from "axios";
import ChartWrapper from "./ChartWrapper.vue";
import JSON5 from "json5";

export default {
  name: "EchartsDemo",
  components: {
    ChartWrapper,
  },
  data() {
    return {
      charts: {
        bar: null,
        line: null,
        pie: null,
      },
      inputText: "",
      chartData: {},
    };
  },
  mounted() {
    // this.initCharts();
  },
  methods: {
    async sendRequest() {
      try {
        const response = await axios.post("http://localhost:5001/ask", {
          question: this.inputText,
        });
        console.log(
          "Received response:",
          response.data.output.choices[0].message.content
        );
        this.chartData = JSON5.parse(
          response.data.output.choices[0].message.content
        );
        // this.updateCharts();
      } catch (error) {
        console.error("Error:", error);
        this.chartData = {};
      }
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
.chart {
  width: 45%;
  height: 300px;
  margin-bottom: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
.no-data {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  font-size: 18px;
  color: #999;
}
</style>
