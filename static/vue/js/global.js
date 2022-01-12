const sidebar = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            counterNotification: 0,
            counterMessage: 0,
            results: [],
            code: null,
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
                    // if (data["message"] == false) {
                    //     this.SendSms();
                    // }

                });

        },
        SendSms() {
            fetch("/api/Send_code/")
                .then(response => response.json())
                .then((data) => {
                    document.getElementById("numberCheck").onclick();
                });
        },
        sendNumber() {
            if (this.code != null) {
                fetch(`/api/CountReadStatus/${this.code}`)
                    .then(response => response.json())
                    .then((data) => {

                    });
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