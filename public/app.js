const SERVER_URL = "http://localhost:8080"

Vue.createApp({
  data: function () {
    return {
      events: [],
      eventTitle: "",
      eventLocation: "",
      eventDate: "",
      eventStartTime: "",
      eventEndTime: "",
      eventType: "",
      eventDesc: "",
      expandedEvent: "",
      showStandard: true,
      showCreateEvent: false,
      showExpandedEvent: false
    };
  },
  methods: {
    createEventButton: function() {
      var data = "title=" + encodeURIComponent(this.eventTitle);
      data += "&location=" + encodeURIComponent(this.eventLocation);
      data += "&date=" + encodeURIComponent(this.eventDate);
      data += "&start_time=" + encodeURIComponent(this.eventStartTime);
      data += "&end_time=" + encodeURIComponent(this.eventEndTime);
      data += "&type=" + encodeURIComponent(this.eventType);
      data += "&desc=" + encodeURIComponent(this.eventDesc);

      fetch(SERVER_URL + "/events", {
        method: "POST",
        body: data,
        headers: {
        "Content-Type": "application/x-www-form-urlencoded"
        }
      }).then((response) => {
        if (response.status == 201) {
          this.getEvents();
          console.log("Event created:", this.eventTitle);
          this.eventTitle = "";
          this.eventLocation = "";
          this.eventDate = "";
          this.eventStartTime = "";
	  this.eventEndTime = "";
          this.eventType = "";
	  this.eventDesc = "";
          } else {
            console.error("Failed to create event on server");
          }
      });
      this.showCreateEvent = false;
      this.showStandard = true;
    },
    getEvents: function () {
      fetch(SERVER_URL + '/events').then((response) => {
        response.json().then((data) => {
          console.log("loaded events from the server:", data);
          this.events = data;
        });
      });  
    },
    expandEvent: function (event) {
      this.getSingleEvent(event._id);
      this.showStandard = false;
      this.showExpandedEvent = true;
    },
    gotoCreateEvent: function () {
      this.showStandard = false;
      this.showCreateEvent = true;
    },
    getSingleEvent: function (eventID) {
      fetch(SERVER_URL + "/events/" + eventID).then((response) => {
        response.json().then((data) => {
          this.expandedEvent = data;
        });
      });
    }

  },

  created: function () {
    this.getEvents();
  }


}).mount("#app");
