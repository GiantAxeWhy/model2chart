<template>
  <div class="chart-wrapper">
    <div v-show="hasData && !isRenderingFailed" ref="chart" class="chart"></div>
    <div v-show="!hasData || isRenderingFailed" class="no-data">暂无数据</div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "ChartWrapper",
  props: {
    chartData: {
      type: Object,
      required: true,
    },
    chartType: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
      isRenderingFailed: false,
    };
  },
  computed: {
    hasData() {
      return (
        this.chartData &&
        this.chartData.xAxis &&
        this.chartData.yAxis &&
        this.chartData.xAxis.length > 0 &&
        this.chartData.yAxis.length > 0
      );
    },
  },
  watch: {
    chartData: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.$nextTick(() => {
            this.updateChart();
          });
        }
      },
      deep: true,
    },
    chartType(newType, oldType) {
      if (newType !== oldType) {
        this.updateChart();
      }
    },
  },
  mounted() {
    this.initChart();
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    initChart() {
      if (this.hasData && this.$refs.chart) {
        this.chart = echarts.init(this.$refs.chart);
        this.updateChart();
      }
    },
    updateChart() {
      if (!this.hasData) {
        if (this.chart) {
          this.chart.dispose();
          this.chart = null;
        }
        return;
      }

      if (!this.chart && this.$refs.chart) {
        this.chart = echarts.init(this.$refs.chart);
      }

      try {
        const option =
          this[
            `get${
              this.chartType.charAt(0).toUpperCase() + this.chartType.slice(1)
            }Option`
          ]();
        this.chart.setOption(option);
      } catch (error) {
        console.error("ECharts rendering failed:", error);
        if (this.chart) {
          this.chart.dispose();
        }
        this.chart = null;

        this.isRenderingFailed = true;
      }
    },
    getBarOption() {
      return {
        title: { text: "负面反馈趋势 (柱状图)" },
        tooltip: { trigger: "axis" },
        xAxis: { type: "category", data: this.chartData.xAxis },
        yAxis: { type: "value", name: "负面反馈数量" },
        series: [{ data: this.chartData.yAxis, type: "bar", name: "负面反馈" }],
      };
    },
    getLineOption() {
      return {
        title: { text: "负面反馈趋势 (折线图)" },
        tooltip: { trigger: "axis" },
        xAxis: { type: "category", data: this.chartData.xAxis },
        yAxis: { type: "value", name: "负面反馈数量" },
        series: [
          { data: this.chartData.yAxis, type: "line", name: "负面反馈" },
        ],
      };
    },
    getPieOption() {
      const pieData = this.chartData.xAxis.map((month, index) => ({
        name: month,
        value: this.chartData.yAxis[index],
      }));
      return {
        title: { text: "负面反馈分布 (饼图)" },
        tooltip: { trigger: "item" },
        series: [
          {
            type: "pie",
            radius: "50%",
            data: pieData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
}
.chart {
  width: 100%;
  height: 100%;
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
