const home = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            postPage: 1,
            results: [],
            selfUser: "",
            loading: true
        }
    },
    methods: {
        getDataHome() {
            fetch(`/api/HomeApiView/?page=${this.postPage}`)
                .then(response => response.json())
                .then((data) => {
                    data.forEach(element => this.results.push(element))
                    if (data.length == 0) this.loading = false
                });
        },
        handleScroll() {
            if (document.body.scrollHeight - window.scrollY <= 1000) {
                this.postPage += 1
                this.getDataHome();
                this.wait(100)
            }
        },
        async like(id, index) {
            await fetch(`/api/AddLikeView/?Picture=${id}`)
            if (this.results[index].data.likeAuthor == true) {
                this.results[index].data.likeAuthor = false
                this.results[index].data.like_count--
            } else {
                this.results[index].data.likeAuthor = true
                this.results[index].data.like_count++
            }

        },
        async deleteRequest(id, index) {
            await fetch(`/api/DestroyRequestApi/${id}/`, {
                method: "delete",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    'X-CSRFToken': window.CSRF_TOKEN
                }
            })
            this.results.splice(index, 1);
        },
        async deletePicture(id, index) {
            await fetch(`/api/PicturePostDestroyRetrive/${id}/`, {
                method: "delete",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    'X-CSRFToken': window.CSRF_TOKEN
                }
            })
            this.results.splice(index, 1);
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
        this.getDataHome();
        this.selfUser = document.getElementById('SelfInformation').innerHTML
        window.addEventListener('scroll', this.handleScroll);
    }
}
Vue.createApp(home).mount('#home')