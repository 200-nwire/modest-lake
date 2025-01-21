
const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');
const { CubejsApi } = require('@cubejs-client/core');

const app = new Koa();
const router = new Router();

const cubejsApi = new CubejsApi('http://cubejs:4000', { headers: {} });

router.get('/metrics', async (ctx) => {
  const query = {
    measures: ['NetworkTraffic.totalBytes'],
    dimensions: ['NetworkTraffic.srcIp'],
    limit: 10,
  };
  ctx.body = await cubejsApi.load(query);
});

app.use(bodyParser());
app.use(router.routes());
app.use(router.allowedMethods());

app.listen(4000, () => console.log('API running on http://localhost:4000'));
