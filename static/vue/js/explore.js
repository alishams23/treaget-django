const explore = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            picturePage: 1,
            ProjectPage: 1,
            counterMessage: 0,
            search: "",
            UsersData: [],
            results: [],
            resultsProject: [],
            userInfo: document.getElementById("SelfInformation").innerHTML,
            userInfoStatus: document.getElementById("SelfInfoServiceProvider").innerHTML,
            page: 0,
        }
    },
    methods: {
        searchModel(data) {
            this.UsersData = []
            this.results = []
            this.resultsProject = [
                []
            ]
            if (this.search != "") {
                this.getDataExplore()
                this.searchExploreProject()
                this.searchUser()
            } else {
                this.getDataExplore()
                this.getDataExploreProject()
                this.searchUser()
            }
        },
        getDataExplore() {
            fetch("/api/ExploreApiView/")
                .then(response => response.json())
                .then((data) => {
                    this.picturePage == 1 ? this.results.push(data) : data.forEach(element => this.results[0].push(element))
                });
        },
        searchUser() {
            fetch(`/api/UserSearchListApi/?search=${this.search}`)
                .then(response => response.json())
                .then((data) => {
                    data["results"].forEach(element => this.UsersData.push(element))
                });
        },
        userClick() {
            this.page = 2
            this.searchUser()
        },
        getDataExploreProject() {
            fetch(`/api/ExploreProjectApiView/?page=${this.ProjectPage}`)
                .then(response => response.json())
                .then((data) => {
                    this.ProjectPage == 1 ? this.resultsProject.push(data["results"]) : data["results"].forEach(element => this.resultsProject[0].push(element));
                });
        },
        searchExploreProject() {
            fetch(`/api/RequestSearchApi/?search=${this.search}`)
                .then(response => response.json())
                .then((data) => {
                    data["results"].forEach(element => this.resultsProject[0].push(element));
                });
        },
        handleScroll(event) {
            console.log(this.results[0].length)
            if (document.body.scrollHeight - window.scrollY <= 1000 && this.page == 0) {
                this.picturePage += 1
                this.getDataExplore();
                this.wait(100)

            } else if (document.body.scrollHeight - window.scrollY <= 1000 && this.page == 1) {
                this.ProjectPage += 1
                this.getDataExploreProject();
                this.wait(100)

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
        this.getDataExploreProject();
        window.addEventListener('scroll', this.handleScroll);

    },

}
Vue.createApp(explore).mount('#explore')