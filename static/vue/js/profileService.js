const profile = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            service: [],
            loading: true,
            selfUser: document.getElementById('SelfInformation').innerHTML,
            selfUserService: document.getElementById('SelfInfoServiceProvider').innerHTML

        }
    },
    methods: {
        ServiseApi() {
            fetch(`/api/ServiceListApi/${document.getElementById('service').getAttribute('value')}/`)
                .then(response => response.json())
                .then((data) => {
                    this.service = data;
                    this.loading = false;
                    console.log(data);
                });
        },
    },
    mounted() {
        this.ServiseApi();
    }
}
Vue.createApp(profile).mount('#service')