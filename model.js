const sqlite3 = require('sqlite3').verbose();


tempData = []

addEvent: function addEvent(event) {
  // TODO
  let db = new sqlite3.Database('./db/events.db');

  return new Promise((resolve, reject) => {
    if (!event.name || !event.location || !event.date || !event.time || !event.type) {
      reject(new Error('Missing information'));
    }
    db.run('INSERT INTO events (name, location, date, start_time, end_time, type, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [event.name, event.location, event.date, event.start_time, event.end_time, event.type, event.latitude, event.longitude], (err) => {
      if (err) {
        reject(err);
      }
      resolve();
      db.close();
    });
  });
}

getEvents: function getEvents() {
  console.log("made it to getEvents");
  let db = new sqlite3.Database('./db/events.db');
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM events', [], (err, rows) => {
      if (err) {
        console.log("error in getEvents");
        reject(err);
      }
      resolve(rows);
      console.log("getEvents resolved");
      db.close();
    });
  });
}

getSingleEvent: function getSingleEvent(event) {
  let db = new sqlite3.Database('./db/events.db');
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM events WHERE id = ?', [event], (err, rows) => {
      if (err) {
        reject(err);
      }
      resolve(rows);
      db.close();
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
