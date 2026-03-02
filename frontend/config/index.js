import { defineConfig } from '@tarojs/cli'

export default defineConfig({
  projectName: 'bilibili-ai-video',
  date: '2024-01-01',
  designWidth: 750,
  deviceRatio: {
    375: 2,
    640: 2.75,
    750: 1,
    828: 1.81
  },
  sourceRoot: 'src',
  outputRoot: 'dist',
  plugins: [],
  framework: 'react',
  mini: {},
  h5: {
    publicPath: '/',
    staticDirectory: 'static',
    router: {
      mode: 'hash',
      customRoutes: {}
    }
  }
})
