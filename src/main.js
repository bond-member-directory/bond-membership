import { createApp } from 'vue'
import App from './App.vue'
import 'tachyons/css/tachyons.min.css'
import router from './router'
import VueGtag from "vue-gtag-next";

const app = createApp(App);

app.use(router);

const GA_ID = process.env.VUE_APP_GOOGLE_ANALYTICS_ID;
if(GA_ID){
    app.use(VueGtag, {
        property: {
            id: GA_ID,
        }
    }, router);
}

app.mount('#app')
