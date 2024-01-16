import { createApp } from 'vue'
import App from './App.vue'
import 'tachyons/css/tachyons.min.css'
import router from './router'
import { createGtm } from '@gtm-support/vue-gtm'

const app = createApp(App);

app.use(router);

const GTM_ID = process.env.VUE_APP_GTM_ID;
if (GTM_ID) {
    app.use(
        createGtm({
            id: GTM_ID,
            vueRouter: router,
            debug: process.env.NODE_ENV === 'development',
            trackOnNextTick: true,
        }),
    );
}

app.mount('#app')
