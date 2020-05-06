import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueNumberInput from '@chenfengyuan/vue-number-input';
import FlashMessage from '@smartweb/vue-flash-message';
import { Datetime } from 'vue-datetime';
import { BFormFile } from 'bootstrap-vue'
import StarRating from 'vue-star-rating'

Vue.component('star-rating', StarRating);
Vue.component('b-form-file', BFormFile);
Vue.use(Datetime);
Vue.use(FlashMessage);
Vue.use(VueNumberInput);
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

var filter = function(text, length, clamp){
    clamp = clamp || '...';
    var node = document.createElement('div');
    node.innerHTML = text;
    var content = node.textContent;
    return content.length > length ? content.slice(0, length) + clamp : content;
};

Vue.filter('truncate', filter);
