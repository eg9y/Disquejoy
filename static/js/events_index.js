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

    // // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};

    function get_memos_url(start_idx, end_idx) {
      var pp = {
        start_idx: start_idx,
        end_idx: end_idx
      };
      return hookToEvents + "?" + $.param(pp);
    }

    self.delete_member = function(id, user, idofelem) {
      $.post(deleteMember, {id:id, user:user}, function() {
        self.vue.rows_of_members = self.vue.rows_of_members.filter(e => (e.id != idofelem));
      })};

      self.get_memos = function () {
        $.getJSON(get_memos_url(0, 10), function (data) {
          console.log(data);
          self.vue.eventsArr = data.events;
          // self.vue.has_more = data.has_more;
          // self.vue.logged_in = data.logged_in;
          // enumerate(self.vue.eventsArr);
        })
      };


      self.delete = function(){
        $.post(del, {}, function(data){
          console.log(data)  })};


        self.delete_memo = function(memo_idx) {
          $.post(del_memo_url,
            { id: memo_idx },
            function () {
              self.vue.eventsArr = self.vue.eventsArr.filter(e => e.id != memo_idx)
            }
            )

        };

        function markEventsArr() {

          if(self.vue.events_user_is_in.length == 0) {
            for(var k = 0;k<self.vue.eventsArr.length;k++) {
              self.vue.eventsArr[k]["is_member_not_organizer"] = false;
            }
          }
          for(var i = 0;i<self.vue.eventsArr.length;i++) {
            for(var j = 0;j<self.vue.events_user_is_in.length;j++) {
              //console.log(self.vue.eventsArr[i].id);
              if(parseInt(self.vue.eventsArr[i].id) == parseInt(self.vue.events_user_is_in[j].id_of_event) && self.vue.eventsArr[i].organizer_id != self.vue.id_of_current_user) {
                self.vue.eventsArr[i]["is_member_not_organizer"] = true;
              }
              else {
                console.log("Entered");
                self.vue.eventsArr[i]["is_member_not_organizer"] = false;
              }
            }
          }
          console.log(self.vue.eventsArr);

        }

        function get_events_user_is_registered_in() {
          if(self.vue.id_of_current_user == "") {
            get_current_user();
          }
          $.post(get_current_user_events, {id:self.vue.id_of_current_user}, function(data) {
            console.log(data.rows);
            self.vue.events_user_is_in = data.rows;
            markEventsArr();
          })
        }


        function get_current_user() {
         $.post(get_current_user_informations, {}, function(data) {
          self.vue.id_of_current_user = data.results["id"];
          self.vue.name_of_current_user = data.results["display_name"];
          get_events_user_is_registered_in();

        })
       }

       self.select_event_to_display_members = function (memo_idx) {
         self.vue.is_commenting = null;
        var index = 0;
        for(var i = 0;i<self.vue.eventsArr.length;i++) {
          if(self.vue.eventsArr[i].id == memo_idx) {
            index = i;
            break;
          }
        }

        self.vue.is_viewing_members = !self.vue.is_viewing_members;
        self.vue.selected_id_to_display_members = self.vue.eventsArr[index].id;

        $.post(get_events_members, {id:memo_idx},function(data) {
          self.vue.rows_of_members = data.rows;
          console.log(self.vue.rows_of_members);
        })
      };

      self.comment_memo_button = function (memo_idx) {
       // The button to edit a memo has been pressed.
       self.vue.is_viewing_members = null;
       var index = 0;
       for(var i = 0;i<self.vue.eventsArr.length;i++) {
         if(self.vue.eventsArr[i].id == memo_idx) {
           index = i;
           break;
         }
       }

       self.vue.is_commenting = !self.vue.is_commenting;
       self.vue.selected_comment_id = self.vue.eventsArr[index].id;

        $.post(get_comments, {id:memo_idx},function(data) {
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
       for(var i = 0;i<self.vue.eventsArr.length;i++) {
         if(self.vue.eventsArr[i].id == memo_idx) {
           index = i;
           break;
         }
       }

       $.post(add_comment, {
         typeComment:"EVENT",
         id:memo_idx,
         commentText: self.vue.comment,
       },function(data) {
         self.vue.comments.push({
           comment_type:"EVENT",
           commentText:self.vue.comment,
           id_comment_belongs_to: memo_idx,
           pictureOfCommenter: data.spotify_user["image"],
           nameOfCommenter:self.vue.name_of_current_user,
           idOfCommenter: data.spotify_user["username"]
         })
         self.vue.eventsArr[i].numberOfCommentsInFeed = parseInt(self.vue.eventsArr[i].numberOfCommentsInFeed) + 1;
         self.vue.comment = "";
       })

     }

     self.comment_memo = function (memo_idx) {
       self.vue.comments.clear();
      // The button to edit a memo has been pressed.
      var index = 0;
      for(var i = 0;i<self.vue.eventsArr.length;i++) {
        if(self.vue.eventsArr[i].id == memo_idx) {
          index = i;
          break;
        }
      }
      self.vue.is_commenting = !self.vue.is_commenting;
      self.vue.selected_comment_id = self.vue.eventsArr[index].id;
      self.vue.locationOfEvent = self.vue.eventsArr[index].Area;
    };


      self.edit_memo_button = function (memo_idx) {
       // The button to edit a memo has been pressed.
       var index = 0;
       for(var i = 0;i<self.vue.eventsArr.length;i++) {
         if(self.vue.eventsArr[i].id == memo_idx) {
           index = i;
           break;
         }
       }
       console.log('memo id: ' + memo_idx);
       console.log(self.vue.eventsArr[index]);

       self.vue.is_editing_memo = !self.vue.is_editing_memo;
       self.vue.selected_id = self.vue.eventsArr[index].id;
       self.vue.locationOfEvent = self.vue.eventsArr[index].Area;
     };

     self.edit_memo = function(memo_idx) {
      // The save button to edit a memo has been pressed.
      var index = 0;
      for(var i = 0;i<self.vue.eventsArr.length;i++) {
        if(self.vue.eventsArr[i].id == memo_idx) {
          index = i;
          break;
        }
      }
      console.log('Here' +self.vue.locationOfEvent);
      $.post(update,
      {
        id: self.vue.selected_id,
        title:self.vue.title_inserted,
        locationOfEvent:self.vue.locationOfEvent,
        datetime:self.vue.datetime,
        description: self.vue.description,
        GIFurl: self.vue.GIFurl
      },
      function (data) {
        console.log(data.q);
        self.vue.eventsArr[index].title = self.vue.title_inserted;
        self.vue.eventsArr[index].description = self.vue.description;
        self.vue.eventsArr[index].Area = self.vue.locationOfEvent;
        self.vue.eventsArr[index].GIF = self.vue.GIFurl;
        self.vue.form_edit_title = "";
        self.vue.form_edit_memo = "";
        self.vue.title_inserted = "";
        self.vue.GIFurl = "";
        self.vue.description = "";
        self.vue.locationOfEvent = "";
        self.vue.is_editing_memo = !self.vue.is_editing_memo;
      }
      )
    };

    self.add_member = function(id, name) {
      console.log("entered!!" + id + " " +name);
      $.post(add_member_url, {id:id, name:name}, function(data) {
        console.log(data);
        for(var i = 0;i<self.vue.eventsArr.length;i++) {
          if(parseInt(self.vue.eventsArr[i].id) == id) {
            break;
          }
        }
        self.vue.eventsArr[i].is_member_not_organizer = !self.vue.eventsArr[i].is_member_not_organizer;
        console.log(self.vue.eventsArr);
      })

    }
    self.cancel_edit = function() {
      self.vue.is_editing_memo = false;
    }




    self.vue = new Vue({
      el: "#container",
      delimiters: ['${', '}'],
      unsafeDelimiters: ['!{', '}'],
      data: {
        eventsArr: Array,
        is_viewing_members:false,
        rows_of_members:[],
        is_editing_memo:false,
        locationOfEvent: "",
        datetime:"",
        description:"",
        GIFurl:"",
        title_inserted:"",
        id_of_current_user:"",
        name_of_current_user:"",
        events_user_is_in:[],
        form_edit_title: null,
        form_edit_memo: null,
        gif_edit_url:null,
        is_commenting:false,
        ids_of_comment: [],
        comments:[],
        comment:null,
        selected_comment_id:-1,
        selected_id_to_display_members:-1,
        selected_id: -1  // Saves selected memo ID.
      },
      methods: {
        delete: self.delete,
        delete_memo: self.delete_memo,
        delete_member:self.delete_member,
        add_member:self.add_member,
        select_event_to_display_members:self.select_event_to_display_members,
        cancel_edit:self.cancel_edit,
        edit_memo_button:self.edit_memo_button,
        edit_memo: self.edit_memo,
        comment_memo_button:self.comment_memo_button,
        push_comment:self.push_comment,
      }
    });
    get_current_user();
    self.get_memos();
    $("#container").show();

    return self;
  };

  var APP = null;

  // This will make everything accessible from the js console;
  // for instance, self.x above would be accessible as APP.x
  jQuery(function(){APP = app();});
