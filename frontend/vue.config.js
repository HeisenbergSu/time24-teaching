module.exports = {
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:5000',
        changeOrigin: true
      }
    }
  }
}

