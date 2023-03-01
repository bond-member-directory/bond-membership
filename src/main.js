import { createApp } from 'vue'
import App from './App.vue'
import 'tachyons/css/tachyons.min.css'
import router from './router'
import { createGtm } from '@gtm-support/vue-gtm';

const app = createApp(App);

app.use(router);


const GA_ID = process.env.VUE_APP_GTM_ID;
if (GA_ID) {
    app.use(
        createGtm({
            id: GA_ID,
            vueRouter: router,
        }),
    );
}

app.mount('#app')
