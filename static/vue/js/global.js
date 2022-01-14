const sidebar = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            counterNotification: 0,
            counterMessage: 0,
            results: [],
            code: null,
            statusSend: false,
            statusCheck: false
        }
    },
    methods: {
        CountRead() {
            var result
            fetch("/api/CountReadStatus/")
                .then(response => response.json())
                .then((data) => {
                    this.counterNotification = data["notification"];
                    this.counterMessage = data["message"];
                    if (data["verify_phone"] == false && this.statusSend == false) {
                        this.SendSms();
                    }

                });

        },
        async SendSms() {
            this.statusSend = true
            await fetch("/api/Send_code/")
            document.getElementById("numberCheck").click();
        },
        async sendNumber() {
            try {
                if (this.code != null) {
                    this.statusCheck = false
                    let statusCheckApi = await fetch(`/api/Code_check/?code=${this.code}`)
                    console.log(statusCheckApi.status); // returns 200
                    this.statusCheck = true
                    if (statusCheckApi.ok) {
                        document.getElementById("closeSms").click();
                    }

                }
            } catch (error) {
                this.statusCheck = true
            }


        }
    },
    mounted() {
        this.CountRead();
        setInterval(() => this.CountRead(), 8000);
    }
}
Vue.createApp(sidebar).mount('#sidebar')

function shareLink(dataValue) {
    let input = document.body.appendChild(document.createElement("input"));
    input.value = `${window.location.hostname}/${dataValue}`;
    input.focus();
    input.select();
    document.execCommand('copy');
    input.parentNode.removeChild(input);
    alert(`${window.location.hostname}/${dataValue} کپی شد.`)
}