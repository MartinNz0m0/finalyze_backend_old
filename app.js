const express = require("express");
const app = express();
const cors = require("cors");
const multer = require("multer");
const bodyparser = require("body-parser");
const winston = require("winston");
const register = require("./register");
const login = require("./login");
const dash = require("./dashboard");
const data = require("./data");
const retrieve = require("./retrieve");
const del = require("./delete");
const passport = require("passport");
const upload = require("./upload");
const datar = data.data;
const convert = data.convert;
const uploadcoop = upload.uploadcoop;
const uploadequity = upload.uploadequity;

require("./strat");

const logger = winston.createLogger({
  transports: [new winston.transports.File({ filename: "combined.log" })],
});

app.use(cors());
app.use(bodyparser.json({ type: "application/*+json" }));
const headers = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
};

const filestore = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "./uploads");
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const uploading = multer({
  storage: filestore,
  // filter pdf types
  fileFilter: (req, file, cb) => {
    if (file.mimetype == "application/pdf") {
      cb(null, true);
    } else {
      cb(null, false);
      // return cb(new Error('Only pdf is allowed!'));
    }
  },
});

let arr = [];
let namearr = [];

app.get("/", (req, res) => {
  res.send("Welscome");
});

app.post("/api", uploading.single("file"), (req, res) => {
  res.set(headers);
  if (!req.file) {
    console.log("file error");
    let error = "Wrong filetype";
    let e = JSON.stringify({ error });
    res.json(e);
  }
  let pagesarr = [];
  var name = req.file.originalname;
  var fileinfo = req.file.path;
  namearr.push(name);

  setTimeout(() => {
    d = JSON.stringify({ fileinfo, pagesarr });
    console.log(d);

    res.json(d);
  }, 500);
});

// receive coop file
app.post(
  "/uploadcoop",
  uploading.single("file"),
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next(); // pass the user object to the next middleware function
  },
  uploadcoop
);

// receive equity file
app.post(
  "/uploadequity",
  uploading.single("file"),
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next(); // pass the user object to the next middleware function
  },
  uploadequity
);

app.use(bodyparser.json());
app.post("/csv", convert);

app.post("/data", datar);
app.post(
  "/retrieve",
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next(); // pass the user object to the next middleware function
  },
  retrieve
);


// for login test
app.post("/login", login);
app.post("/register", register);
app.post(
  "/dash",
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next(); // pass the user object to the next middleware function
  },
  dash
);
app.post(
  "/delete",
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next(); // pass the user object to the next middleware function
  },
  del
);
app.post(
  "/verify",
  passport.authenticate("jwt", { session: false }),
  (req, res, next) => {
    next();
  },
  (req, res) => {
    res.status(200).json(req.user);
  }
);

app.listen(8000, () => {
  console.log("Server running on 8000");
});
