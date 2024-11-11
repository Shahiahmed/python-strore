module.exports = {
  content: [
    './templates/**/*.html',
    './store/templates/**/*.html',
    './my_store/templates/**/*.html',
    './orders/templates/**/*.html',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
};
