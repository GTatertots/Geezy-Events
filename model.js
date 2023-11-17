const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./db/events.db');
db.close();

addEvent: function (event) {

}

getEvents: function () {
  db.all('SELECT * FROM events', [], (err, rows) => {
    if (err) {
      throw err;
    }
    rows.forEach((row) => {
      console.log(row.name);
    });
  });
}

getSingleEvent: function (event) {

}

replaceEvent: function (event) {

}

deleteEvent: function (event) {

}

module.exports = {
  addEvent: addEvent,
  getEvents: getEvents,
  getSingleEvent: getSingleEvents,
  replaceEvent: replaceEvent,
  deleteEvent: deleteEvent
};
