const profile = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            service: [],
            loading: true,
            selfUser: document.getElementById('SelfInformation').innerHTML,
            selfUserService: document.getElementById('SelfInfoServiceProvider').innerHTML,
            orderData: "",
            descriptionOrder: "",

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
        order(index) {
            this.orderData = this.service[index]
        },
        plusKey(index, indexOption) {
            if (this.service[index]["price"] == null) this.service[index]["price"] = 0
            this.service[index]["price"] += this.service[index]["serviceFacilities"][indexOption]["price"]
            this.service[index]["serviceFacilities"][indexOption]["isChoice"] = true
        },
        minesKey(index, indexOption) {
            this.service[index]["price"] -= this.service[index]["serviceFacilities"][indexOption]["price"]
            this.service[index]["serviceFacilities"][indexOption]["isChoice"] = false
        },
        sendOrder() {
            fetch(`/api/AddOrderApi/${this.orderData["author"]["username"]}` + "/", {
                    method: "post",
                    credentials: "same-origin",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        'X-CSRFToken': window.CSRF_TOKEN
                    },
                    body: JSON.stringify({ "price": this.orderData["price"], "title": this.orderData["title"], "body": this.descriptionOrder, "service": this.orderData["id"] }),
                }).then(response => response.json())
                .then((data) => {
                    window.location.href = `/account/orders/`
                });
        }
    },
    mounted() {
        this.ServiseApi();
    }
}
Vue.createApp(profile).mount('#service')