const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/ask": {
        target: "http://127.0.0.1:5001",
        changeOrigin: true,
      },
    },
  },
});
