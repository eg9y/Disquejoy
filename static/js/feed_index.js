// This is the js for the default/index.html view.

var app = function (data, device_id, player) {
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
        console.log(data);
      })

    }

    self.hello = function() {
      console.log("Hello!");
    }


    // Complete as needed.
    self.vue = new Vue({
        el: "#parent",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            feedArr: [],

        },
        methods: {
          getFeed: self.getFeed,
          hello:self.hello
        },

    });
    self.getFeed();
    self.hello();
    $("#parent").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
