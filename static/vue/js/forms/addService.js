const addService = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            serviceOption: [],
            showAlert: false,
            priceOption: "",
            optionName: "",
            nameProduct: "",
            priceProduct: "",
            specialName: "",
            selfUser: document.getElementById('SelfInformation').innerHTML,

        }
    },
    methods: {
        changeDiv() {
            let SpecialName = document.querySelector("#specialName");
            let attrSpecialName = SpecialName.getAttribute("hidden");
            let nameProduct = document.querySelector("#nameProduct");
            if (attrSpecialName != null) {
                SpecialName.removeAttribute("hidden");
                nameProduct.setAttribute("hidden", null);
                this.nameProduct = ""
            } else {
                nameProduct.removeAttribute("hidden");
                SpecialName.setAttribute("hidden", null);
                this.specialName = ""
            }
        },
        deleteOption(index) {
            this.serviceOption.splice(index, 1);
        },
        submitModel() {
            fetch("/api/AddOptionService/", {
                    method: "post",
                    credentials: "same-origin",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        'X-CSRFToken': window.CSRF_TOKEN
                    },
                    body: JSON.stringify({ 'title': this.optionName, 'price': parseInt(this.priceOption) }),
                }).then(response => response.json())
                .then((data) => {
                    this.serviceOption.push({ "title": data["title"], "price": data.price, "id": data["id"] })
                });
            this.$refs.btnClose.click()
            this.optionName = ""
            this.priceOption = ""
        },
        submitForm() {
            let dataOption = []
            this.serviceOption.forEach(element => { dataOption.push(element["id"]) })
            fetch("/api/AddService/", {
                    method: "post",
                    credentials: "same-origin",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        'X-CSRFToken': window.CSRF_TOKEN
                    },
                    body: JSON.stringify({ "serviceOption": dataOption, 'nameProduct': parseInt(this.nameProduct), 'price': parseInt(this.priceProduct), "specialName": this.specialName }),
                }).then(response => response.json())
                .then((data) => {
                    window.location.href = `/p/${this.selfUser}/service`
                });
            console.log(this.priceProduct)
            console.log(this.nameProduct)
            console.log(this.specialName)
        }
    },
}
Vue.createApp(addService).mount('#addService')