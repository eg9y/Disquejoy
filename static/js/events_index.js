// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    // self.extend = function(a, b) {
    //     for (var i = 0; i < b.length; i++) {
    //         a.push(b[i]);
    //     }
    // };

    // // Enumerates an array.
    // var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};

    // function get_memos_url(start_idx, end_idx) {
    //     var pp = {
    //         start_idx: start_idx,
    //         end_idx: end_idx
    //     };
    //     return memos_url + "?" + $.param(pp);
    // }

    // self.get_memos = function () {
    //     $.getJSON(get_memos_url(0, 10), function (data) {
    //         self.vue.memos = data.memos;
    //         self.vue.has_more = data.has_more;
    //         self.vue.logged_in = data.logged_in;
    //         enumerate(self.vue.memos);
    //     })
    // };

    // self.get_more = function () {
    //     var num_memos = self.vue.memos.length;
    //     $.getJSON(get_memos_url(num_memos, num_memos + 10), function (data) {
    //         self.vue.has_more = data.has_more;
    //         self.extend(self.vue.memos, data.memos);
    //         enumerate(self.vue.memos);
    //     });
    // };

    // self.add_memo_button = function () {
    //     // The button to add a memo has been pressed.
    //     self.vue.is_adding_memo = !self.vue.is_adding_memo;
    // };

    // self.add_memo = function () {
    //     // The submit button to add a memo has been pressed.
    //     $.post(add_memo_url,
    //         {
    //             title: self.vue.form_title,
    //             memo: self.vue.form_memo
    //         },
    //         function (data) {
    //             $.web2py.enableElement($("#add_memo_submit"));
    //             self.vue.memos.unshift(data.memo);
    //             enumerate(self.vue.memos);
    //             self.vue.form_title = "";
    //             self.vue.form_memo = "";
    //             self.vue.is_adding_memo = !self.vue.is_adding_memo;
    //         });
    // };

    self.delete_memo = function(memo_idx) {
        $.post(del_memo_url,
            { memo_id: self.vue.memos[memo_idx].id },
            function () {
                self.vue.memos.splice(memo_idx, 1);
                enumerate(self.vue.memos);
            }
        )
    };

    self.edit_memo_button = function (memo_idx) {
        // The button to edit a memo has been pressed.
        self.vue.is_editing_memo = !self.vue.is_editing_memo;
        self.vue.selected_id = self.vue.memos[memo_idx].id;
        self.vue.form_edit_title = self.vue.memos[memo_idx].title;
        self.vue.form_edit_memo =self.vue.memos[memo_idx].memo;
    };

    self.edit_memo = function(memo_idx) {
        // The save button to edit a memo has been pressed.
        $.post(edit_memo_url,
            {
                memo_id: self.vue.memos[memo_idx].id,
                title: self.vue.form_edit_title,
                memo: self.vue.form_edit_memo
            },
            function () {
                self.vue.memos[memo_idx].title = self.vue.form_edit_title;
                self.vue.memos[memo_idx].memo = self.vue.form_edit_memo;
                enumerate(self.vue.memos);
                self.vue.form_edit_title = "";
                self.vue.form_edit_memo = "";
                self.vue.is_editing_memo = !self.vue.is_editing_memo;
            }
        )
  };

  self.toggle_visibility = function(memo_idx) {
      $.post(toggle_memo_url,
            { memo_id: self.vue.memos[memo_idx].id },
            function () {
                self.vue.memos[memo_idx].is_public = !self.vue.memos[memo_idx].is_public;
                enumerate(self.vue.memos);
            }
        )
  };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            // is_adding_memo: false,
            // is_editing_memo: false,
            // memos: [],
            // logged_in: false,
            // has_more: false,
            // form_title: null,
            // form_memo: null,
            // form_edit_title: null,
            // form_edit_memo: null,
            // selected_id: -1  // Saves selected memo ID.
        },
        methods: {
            // get_more: self.get_more,
            // add_memo_button: self.add_memo_button,
            // add_memo: self.add_memo,
            // delete_memo: self.delete_memo,
            // select_memo: self.select_memo,
            // edit_memo_button: self.edit_memo_button,
            // edit_memo: self.edit_memo,
            // toggle_visibility: self.toggle_visibility
        }

    });

    // self.get_memos();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});

