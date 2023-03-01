import { createApp } from 'vue'
import App from './App.vue'
import 'tachyons/css/tachyons.min.css'
import router from './router'
import { createGtm } from '@gtm-support/vue-gtm'
import VueGtag from "vue-gtag-next";

const app = createApp(App);

app.use(router);


const GTM_ID = process.env.VUE_APP_GTM_ID;
if (GTM_ID) {
    app.use(
        createGtm({
            id: GTM_ID,
            vueRouter: router,
        }),
    );
}

const GA_ID = process.env.VUE_APP_GOOGLE_ANALYTICS_ID;
if (GA_ID) {
    app.use(VueGtag, {
        property: {
            id: GA_ID,
        }
    });
}

app.mount('#app')
