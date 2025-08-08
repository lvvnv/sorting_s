const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      timeout: 300000,      // 5 минут
      proxyTimeout: 300000, // 5 минут
      onProxyReq: (proxyReq, req, _res) => {
        // Добавляем заголовок для больших файлов
        if (req.body && Buffer.isBuffer(req.body)) {
          proxyReq.setHeader('Content-Length', req.body.length);
        }
      }
    })
  );
};
