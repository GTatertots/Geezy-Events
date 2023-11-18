const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./db/events.db');
db.close();

tempData = []

addEvent: function addEvent(event) {
  // TODO
  return new Promise((resolve, reject) => {
    // db.run('INSERT INTO events (name, location, date, time, type) VALUES (?, ?, ?, ?, ?)', [event.name, event.location, event.date, event.time, event.type], (err) => {
    //   if (err) {
    //     reject(err);
    //   }
    //   resolve();
    // });
    resolve();
  });
}

getEvents: function getEvents() {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM events', [], (err, rows) => {
      if (err) {
        reject(err);
      }
      resolve(rows);
    });
  });
}

getSingleEvent: function getSingleEvent(event) {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM events WHERE id = ?', [event], (err, rows) => {
      if (err) {
        reject(err);
      }
      resolve(rows);
    });
  });
}

replaceEvent: function replaceEvent(event) {
  // TODO
  return new Promise((resolve, reject) => {
    resolve();
  });
}

deleteEvent: function deleteEvent(event) {
  // TODO
  return new Promise((resolve, reject) => {
    resolve();
  });
}

module.exports = {
  addEvent: addEvent,
  getEvents: getEvents,
  getSingleEvent: getSingleEvent,
  replaceEvent: replaceEvent,
  deleteEvent: deleteEvent
};
