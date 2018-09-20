/**
* Polls the backend for the list of unpaginated Tweets.
*/
function fetchTweets() {
    return new Promise(function (resolve, reject) {
        var req = {
            url: '/',
            method: 'get',
            headers: { 'Accept': 'application/json' }
        };
        $.ajax(req).then(resolve).catch(reject)
    });
}

/**
* Creates an instance of our Vue App.
* @param {Array} initialData The initial list of Tweets.
*/
function createApp(initialData) {
    return new Vue({
        el: '#app',
        data: {
            tweets: initialData,
            username: '',
            tweet: '',
        },
        methods: {
            /**
            * Invoked on Form submit, this takes care of calling the
            * backend to create the new Tweet, fetching an updated
            * list of tweets, and clearing the Form.
            */
            handleSubmitTweet: function (event) {
                event.preventDefault();
                var newTweet = {
                    content: this.tweet,
                    author: this.username
                }
                this.postTweet(newTweet)
                    .then(() => {
                        this.updateTweets();
                        this.clearForm();
                    })
                    .catch(err => {
                        console.error(err)
                    })
            },
            /**
            * Deletes the current content of the Form.
            */
            clearForm: function () {
                this.tweet = '';
                this.username = '';
            },
            /**
            * Takes care of updating the UI with the latest
            * list of Tweets.
            */
            updateTweets: function () {
                fetchTweets().then(resp => {
                    this.tweets = resp
                })
            },
            /**
            * Does the actual backend calling, to create a new Tweet.
            * @param {object} newTweet The information required to send
            * to the backend and create a new Tweet.
            */
            postTweet: function (newTweet) {
                return new Promise(function (resolve, reject) {
                    var req = {
                        url: '/',
                        method: 'post',
                        headers: { 'Content-Type': 'application/json' },
                        data: JSON.stringify(newTweet),
                    }
                    $.ajax(req).then(resolve).catch(reject);
                });
            },
        }
    })
}

var app;
(function init() {
    fetchTweets()
        .catch(console.error)
        .then((resp) => {
            app = createApp(resp)
        })
})()