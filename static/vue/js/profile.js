const profile = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            picture: [],
            loading: true,
        }
    },
    methods: {
        PictureApi() {
            fetch(`/api/PicturePostListApi/${document.getElementById('profile').getAttribute('value')}/`)
                .then(response => response.json())
                .then((data) => {
                    this.picture = data;
                    this.loading = false;
                    console.log(data);
                });

        },
        PictureUrl(data) {
            var newStr = data.slice(0, -3);
            return newStr;
        }
    },
    mounted() {
        this.PictureApi();
    }
}
Vue.createApp(profile).mount('#profile')