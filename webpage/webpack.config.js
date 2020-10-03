const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');
const GoogleFontsPlugin = require('google-fonts-plugin');

module.exports = {
  mode: 'production',
  //mode: 'development',
  entry: {
    app: './page/src/index.ts'
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        loader: 'ts-loader',
        options: { appendTsSuffixTo: [/\.vue$/] }
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          //'style-loader',
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: '/static/',
            }
          },
          'css-loader',
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass'),
              sassOptions: {
                fiber: require('fibers'),
                indentedSyntax: true
              }
            }
          }
        ]
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: [
          'file-loader'
        ]
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: '/static/',
            }
          },
          'css-loader',
        ]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: 'file-loader'
      }
    ]
  },
  resolve: {
    extensions: ['.ts', '.vue', '.js']
  },
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'public/static'),
    publicPath: "./static",
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      inject: false,
      template: require('html-webpack-template'),
      appMountId: 'app',
      mobile: true,
      lang: 'zh-CN',
      meta: [
        {
          name: 'description',
          content: 'pl-log-notic'
        }
      ],
      title: 'pl-log-notic',
      window: {
        env: {
          apiHost: '' // http://www.yourhost.com
        }
      }
    }),
    new VueLoaderPlugin(),
    new webpack.WatchIgnorePlugin([
      /\.js$/,
      /\.d\.ts$/
    ]),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
      ignoreOrder: false, // Enable to remove warnings about conflicting order
    }),
    new VuetifyLoaderPlugin({
      match (originalTag, { kebabTag, camelTag, path, component }) {
        if (kebabTag.startsWith('core-')) {
          return [camelTag, `import ${camelTag} from '@/components/core/${camelTag.substring(4)}.vue'`]
        }
      }
    }),
    new GoogleFontsPlugin({
      filename: "[chunkhash].css"
      //encode: false
    })
  ],
  optimization: {
    moduleIds: 'hashed',
    runtimeChunk: 'single',
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        }
      }
    }
  }
};
