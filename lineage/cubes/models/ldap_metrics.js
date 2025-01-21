cube(`LdapMetrics`, {
    sql: `SELECT * FROM analytics.ldap_summary`,

    measures: {
        totalEvents: {
            sql: `total_events`,
            type: `sum`,
        },
    },

    dimensions: {
        sourcetype: {
            sql: `sourcetype`,
            type: `string`,
        },
        lastEventTime: {
            sql: `last_event_time`,
            type: `time`,
        },
    },
});
