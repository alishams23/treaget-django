const home = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            postPage: 1,
            results: [],
            selfUser: ""
        }
    },
    methods: {
        getDataExplore() {
            fetch(`/api/HomeApiView/?page=${this.postPage}`)
                .then(response => response.json())
                .then((data) => {
                    data.forEach(element => this.results.push(element))
                    console.log(this.results)
                });
        },
        handleScroll() {
            if (document.body.scrollHeight - window.scrollY <= 1000) {
                this.postPage += 1
                this.getDataExplore();
                this.wait(100)
            }
        },
        like(id) {
            fetch(`/api/AddLikeView/?Picture=${id}`)
                .then(response => response.json())
                .then((data) => {
                    svgChannged = document.getElementById($(this).attr("value"));
                    if (svgChannged.getAttribute("fill") == "blue") {
                        svgChannged.setAttribute("fill", "");
                    } else {
                        svgChannged.setAttribute("fill", "blue");
                    }
                });

        },
        checkLike(data) {
            for (const item of data["like"]) {
                if (item["username"] == this.userInfo) {
                    return true
                } else {
                    return false
                }

            }
        },
        wait(ms) {
            var start = new Date().getTime();
            var end = start;
            while (end < start + ms) {
                end = new Date().getTime();
            }
        },
        shareLink(dataValue) {
            let input = document.body.appendChild(document.createElement("input"));
            input.value = `${window.location.hostname}/${dataValue}`;
            input.focus();
            input.select();
            document.execCommand('copy');
            input.parentNode.removeChild(input);
            alert(`${window.location.hostname}/${dataValue} کپی شد.`)
        }
    },
    mounted() {
        this.getDataExplore();
        this.selfUser = document.getElementById('SelfInformation').innerHTML
            // window.addEventListener('scroll', this.handleScroll);
    }
}
Vue.createApp(home).mount('#home')