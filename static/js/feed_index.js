// This is the js for the default/index.html view.

var app = function () {
    var url = "{{=URL('default', 'index')}}";
    var self = {};
    var musicArray = [];
    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.getFeed= function(){
      $.post(feedURL, {

      }, function(data){
        self.vue.feedArr = data.feed
        console.log(data);
      })

    }

    function getUserInfo() {
          $.post(getUserInfoFromFeed, {}, function(data) {
            console.log(data);
            self.vue.user_name_of_logged_in_user = data.results["display_name"];
            self.vue.id_of_user = data.results["id"];
            //self.getFeed();
            self.get_feed_user_likes();
          })
        }

        self.likeFeed = function(id) {
          for(var i = 0;i<self.vue.feedArr.length;i++) {
            if(self.vue.feedArr[i].id === id) {
              break;
            }
          }
          console.log(self.vue.feedArr[i]);
          console.log(self.vue.user_name_of_logged_in_user);
          console.log(self.vue.id_of_user);
          $.post(likeURL, {
            id:self.vue.feedArr[i].id,
            username:self.vue.user_name_of_logged_in_user,
            typefeed: self.vue.feedArr[i].feed_type,
            userid:self.vue.id_of_user,
          }, function(data) {
            if(data.selectedAgain == null) {
              self.vue.feedArr[i].user_liked = false;
            }
            else{
              self.vue.feedArr[i].user_liked = true;
            }
            self.get_feed_user_likes();
            //self.vue.feedArr2 = self.vue.feedArr;
            console.log(self.vue.feedArr[i].user_liked);
          })
        }
        self.get_feed_user_likes = function() {
          console.log(self.vue.id_of_user);
          $.post(getUserFeedLikes, {userid:self.vue.id_of_user}, function(data) {
            self.vue.arrUserLiked = data.selected;
            console.log(data.selected);
            if(self.vue.arrUserLiked.length == 0) {
              for(var i = 0;i<self.vue.feedArr.length;i++) {
                      self.vue.feedArr[i]["user_liked"] = false;
              }
            }
            else {
              for(var i = 0;i<self.vue.feedArr.length;i++) {
                for(var j = 0;j<self.vue.arrUserLiked.length;j++) {
                    if(parseInt(self.vue.feedArr[i].id) === parseInt(self.vue.arrUserLiked[j].id_of_feed)) {
                        self.vue.feedArr[i]["user_liked"] = true;

                    }

                }
              }
            }
            self.vue.feedArr2 = self.vue.feedArr;
            console.log(self.vue.feedArr2);
          })
        }


    // Complete as needed.
    self.vue = new Vue({
        el: "#parent",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            feedArr: [],
            feedArr2: [],
            arrUserLiked: [],
            id_of_user: null,
            user_name_of_logged_in_user: null
        },
        methods: {
          getFeed: self.getFeed,
          likeFeed: self.likeFeed,
          get_feed_user_likes: self.get_feed_user_likes,
          getUserInfo: getUserInfo
        },

    });
    self.getFeed();
    getUserInfo();
    $("#parent").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
