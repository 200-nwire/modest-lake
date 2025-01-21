
cube(`NetworkTraffic`, {
  sql: `SELECT * FROM iceberg.silver.network_data`,

  measures: {
    count: {
      type: `count`,
      drillMembers: [srcIp, destIp]
    },
    totalBytes: {
      sql: `bytes`,
      type: `sum`
    }
  },

  dimensions: {
    srcIp: {
      sql: `src_ip`,
      type: `string`
    },
    destIp: {
      sql: `dest_ip`,
      type: `string`
    },
    timestamp: {
      sql: `timestamp`,
      type: `time`
    }
  }
});
