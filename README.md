# bond-membership

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Update data from salesforce and charitybase

Include environmental variables:

```
SALESFORCE_CLIENT_ID=<api_id>
SALESFORCE_CLIENT_SECRET=<api_secret>
SALESFORCE_USERNAME=<username>
SALESFORCE_PASSWORD=<password>
SALESFORCE_URL=<salesforce_url>

CHARITYBASE_API_KEY=<apikey>
```

Install requirements:

```bash
pip install -r requirements.txt
```

Fetch data from Salesforce:

```bash
python fetch-data
```
