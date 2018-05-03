// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div22",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        props: ['artist_name'],['artist_title'], ['popularity'], ['']
        data: {
            has_more: false,
            columns: ['name', 'age']
        },
        methods: {
            get_more: self.get_more
        }

    });


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
