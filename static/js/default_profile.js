var app = function() {
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

    function findUsername(id) {
      var email = null;
      $.post(discoverData, {
        id:id
      }, function(data) {
          console.log(data);
      })
        return email;
    }

    self.userTotalLikes = function() {
      //var sum = 0;
      //self.vue.totNumLikesReceived = data.totNumLikesReceived;
      $.post(totLikes, {}, function(data){
        self.vue.tracksUserUploaded = data.tracksUserUploaded;
        for(var i = 0;i<data.tracksUserUploaded.length;i++) {
          self.vue.totNumLikesReceived += data.tracksUserUploaded[i].upvotes;
          self.vue.totNumSongsUploaded += 1;
        }
        console.log(data.tracksUserUploaded);
      })
    }

    self.songsUserLikes = function() {
      $.post(givenLikes, {}, function(data){
            self.vue.countLikesOfUserUploaded = data.retrieveTotalLikesGiven;
          console.log(self.vue.countLikesOfUserUploaded);
        })
      }

      self.songsLikesReceived = function() {
        $.post(receivedLikes, {}, function(data){
              for(var i = 0;i<data.retrieveTotalLikesReceived.length;i++) {
                if(data.retrieveTotalLikesReceived[i].upvoter === null)
                  data.retrieveTotalLikesReceived[i].upvoter = "Anonymous User";
              }
              self.vue.ReceivedUserLikes =  data.retrieveTotalLikesReceived;
          })
        }

    // Complete as needed.
    self.vue = new Vue({
        el: "#parent",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            tracksUserUploaded: Array,
            countLikesOfUserUploaded: Array,
            ReceivedUserLikes: Array,
            totNumLikesReceived: 0,
            totNumSongsUploaded: 0,
            totNumLikesGiven: 0
        },
        methods: {
          userTotalLikes: self.userTotalLikes,
    },

    });
    self.userTotalLikes();
    self.songsUserLikes();
    self.songsLikesReceived();
    $("#parent").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});