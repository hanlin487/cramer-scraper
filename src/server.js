const sqlite3 = require("sqlite3").verbose();
const express = require("express");
const app = express();
const db = new sqlite3.Database("../storage/tweets.db");
const cors = require("cors");

app.use(cors());
app.use(express.static("public"));

app.get("/data", (req, res) => {
  db.all("SELECT * FROM tweets", [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));
