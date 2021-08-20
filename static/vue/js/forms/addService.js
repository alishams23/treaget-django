const addService = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            serviceOption: [],
            showAlert: false,
            priceOption: "",
            optionName: "",
            nameProduct: "",
            priceProduct: ""
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
            } else {
                nameProduct.removeAttribute("hidden");
                SpecialName.setAttribute("hidden", null);
            }
        },
        deleteOption(index) {
            this.serviceOption.splice(index, 1);
        },
        submitModel() {
            this.serviceOption.push([this.optionName, this.priceOption])
            console.log(this.serviceOption)
            this.$refs.btnClose.click()
            this.optionName = ""
            this.priceOption = ""
        }
    },
}
Vue.createApp(addService).mount('#addService')