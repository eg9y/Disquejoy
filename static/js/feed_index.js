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
      id:parseInt(self.vue.feedArr[i].id),
      username:self.vue.user_name_of_logged_in_user,
      typefeed: self.vue.feedArr[i].feed_type,
      userid:self.vue.id_of_user,

    }, function(data) {
      console.log(data);
      if(data.selectedAgain == "deleted") {
        self.vue.ids_of_feed_user_liked =  self.vue.ids_of_feed_user_liked.filter(e => e != self.vue.feedArr[i].id);
      }
      else {
        self.vue.ids_of_feed_user_liked.push(parseInt(data.selectedAgain[0].id_of_feed));
      }
      console.log(self.vue.ids_of_feed_user_liked);
      self.vue.liked = self.vue.ids_of_feed_user_liked.includes(self.vue.feedArr[i].id);
    })
  }


  self.get_feed_user_likes = function() {
    //console.log(self.vue.id_of_user);
    $.post(getUserFeedLikes, {userid:self.vue.id_of_user}, function(data) {
      self.vue.arrUserLiked = data.selected;
      for(var i = 0;i<  self.vue.arrUserLiked.length;i++) {
        self.vue.ids_of_feed_user_liked.push(parseInt(self.vue.arrUserLiked[i].id_of_feed))
      }
      console.log(self.vue.ids_of_feed_user_liked);
    })
  }


  self.comment_memo_button = function (memo_idx) {
    // The button to edit a memo has been pressed.
    console.log(memo_idx);
    var index = 0;
    for(var i = 0;i<self.vue.feedArr.length;i++) {
      if(self.vue.feedArr[i].id == memo_idx) {
        index = i;
        break;
      }
    }

    self.vue.is_commenting = !self.vue.is_commenting;
    self.vue.selected_feed_id = self.vue.feedArr[index].id;

    $.post(comments, {id:memo_idx},function(data) {
      self.vue.comments = data.rows;
      console.log(data.rows);
      for(var i = 0;i<self.vue.comments.length;i++) {
        if(!self.vue.ids_of_comment.includes(self.vue.comments[i].id)){
          self.vue.ids_of_comment.push(self.vue.comments[i].id);
        }
      }
      console.log(self.vue.ids_of_comment);
    })
  };


  self.push_comment = function(memo_idx) {
    var index = 0;
    for(var i = 0;i<self.vue.feedArr.length;i++) {
      if(self.vue.feedArr[i].id == memo_idx) {
        index = i;
        break;
      }
    }

    $.post(add_comment, {
      typeComment:"FEED",
      id:memo_idx,
      commentText: self.vue.comment,
    },function(data) {
      self.vue.comments.push({
        comment_type:"FEED",
        commentText:self.vue.comment,
        id_comment_belongs_to: memo_idx,
        pictureOfCommenter: data.spotify_user["image"],
        nameOfCommenter:self.vue.user_name_of_logged_in_user,
        idOfCommenter: data.spotify_user["username"]
      })
      self.vue.comment = "";
    })

  }



  // Complete as needed.
  self.vue = new Vue({
    el: "#parent",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      feedArr: [],
      is_commenting:false,
      selected_feed_id:-1,
      feedArr2: [],
      liked: false,
      ids_of_comment:[],
      comments:[],
      arrUserLiked: [],
      ids_of_feed_user_liked:[],
      id_of_user: null,
      user_name_of_logged_in_user: null,
      comment:null
    },
    methods: {
      getFeed: self.getFeed,
      likeFeed: self.likeFeed,
      get_feed_user_likes: self.get_feed_user_likes,
      getUserInfo: getUserInfo,
      comment_memo_button:self.comment_memo_button,
      push_comment:self.push_comment,
      idSearcher:self.idSearcher,

    },

  });
  self.getFeed();
  getUserInfo();
  self.get_feed_user_likes();
  $("#parent").show();
  return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
