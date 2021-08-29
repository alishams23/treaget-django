const listOrder = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            listOrders: [],
            loading: true,
            selfUser: document.getElementById('SelfInformation').innerHTML,
            orderData: "",
            descriptionOrder: "",

        }
    },
    methods: {
        OrdersApi() {
            fetch(`/api/OrderApi/`)
                .then(response => response.json())
                .then((data) => {
                    this.listOrders = data;
                    this.loading = false;
                    console.log(data);
                });
        },
    },
    mounted() {
        this.OrdersApi();
    }
}
Vue.createApp(listOrder).mount('#listOrder')