
<template>
  <div id="app">
    <h1>Network Metrics</h1>
    <div id="chart" style="height: 400px;"></div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts';

const response = await fetch('http://localhost:4000/metrics');
const data = await response.json();

const chart = echarts.init(document.getElementById('chart'));
chart.setOption({
  title: { text: 'Top Source IPs by Total Bytes' },
  tooltip: {},
  xAxis: {
    type: 'category',
    data: data.map(item => item['NetworkTraffic.srcIp']),
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      name: 'Total Bytes',
      type: 'bar',
      data: data.map(item => item['NetworkTraffic.totalBytes']),
    },
  ],
});
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
</style>
