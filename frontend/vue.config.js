const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  outputDir: 'dist',
  publicPath: '/',
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/app.html',
      filename: 'index.html'
    }
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
