const sidebar = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            counterNotification: 0,
            counterMessage: 0,
            results: []
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
                });

        },
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