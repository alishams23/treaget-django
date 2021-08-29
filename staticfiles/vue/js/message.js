const message = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            persons: [],
            message: [],
            inputData: "",
            windowHeight: window.innerHeight - 350,
            user: "",
            userSelf: document.getElementById("SelfInformation").innerHTML,
            phoneSize: true,
            scrollTag: { "childElementCount": 1 },
            scrollStatus: true,
            counter: 0,
            userUrl: document.getElementById("userUrl").innerText
        }
    },
    methods: {
        ListUserMessageApi() {
            var result
            fetch("/api/ListUserMessageApi/")
                .then(response => response.json())
                .then((data) => {
                    this.persons = data;
                });
        },
        sendMessage() {
            fetch("/api/MassageApi/", {
                method: "put",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    'X-CSRFToken': window.CSRF_TOKEN
                },
                body: JSON.stringify({ 'sender': this.userSelf['username'], 'receiver': this.user["username"], 'text': this.inputData }),

            })
            this.inputData = ""
            this.getMessage()
        },
        getMessage() {
            fetch(`/api/AllMassageApi/?user=${this.user['username']}`)
                .then(response => response.json())
                .then((data) => {
                    this.message = data;
                });
            this.scrollStatus = true;
            this.counter = 0
            setInterval(() => this.scrollMessage(), 400);
        },
        getMessageRepeat() {
            fetch(`/api/AllMassageApi/?user=${this.user['username']}`)
                .then(response => response.json())
                .then((data) => {
                    this.message = data;
                });
            setInterval(() => this.scrollMessage(), 400);
        },
        getUser() {

            fetch(`/api/UserRetrieveApi/${this.userUrl}`)
                .then(response => response.json())
                .then((data) => {
                    this.user = data;
                    this.getMessage()
                    this.phoneSize = false
                });
            console.log(this.user)
        },
        wait(ms) {
            var start = new Date().getTime();
            var end = start;
            while (end < start + ms) {
                end = new Date().getTime();
            }
        },
        scrollMessage() {
            if ((this.message.length != 0) && (this.scrollStatus == true)) {
                if (this.counter > 1) {

                    var myDiv = document.getElementById("messages-list");
                    myDiv.scrollTop = myDiv.scrollHeight;
                    console.log(this.counter)
                    this.scrollStatus = false;
                }
                this.counter += 1
            }
        },
        getNewMessage() {
            this.counter = 0
            fetch(`/api/MassageApi/?user=${this.user['username']}`)
                .then(response => response.json())
                .then((data) => {
                    data.forEach(element => {
                        this.message.push(element);
                    });
                });
        },
        userClick(info) {
            this.counter = 0
            this.user = info
            this.getMessage()
            setInterval(() => this.getMessageRepeat(), 3000);
        },
    },
    mounted() {
        this.ListUserMessageApi();
        if (this.userUrl != "") {
            this.getUser()
        }
        setInterval(() => this.ListUserMessageApi(), 4000);
    },


}
Vue.createApp(message).mount('#message')