const express = require("express");
const app = express();
const cors = require("cors");
const multer = require("multer");
const Tabula = require("fresh-tabula-js");
const pdfjs = require('pdfjs-dist')
const csv = require("csvtojson");
const appendFileSync = require('fs').appendFileSync
const fs = require('fs')
const bodyparser = require('body-parser');
const winston = require('winston');

const logger = winston.createLogger({
  transports: [
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

app.use(cors());
app.use(bodyparser.json({ type: 'application/*+json'}))
const headers = ({
'Content-Type': 'application/json',
'Access-Control-Allow-Origin': 'https://finalyze.app'
})

const filestore = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "./uploads");
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const uploading = multer({ storage: filestore,
  // filter pdf types
  fileFilter: (req, file, cb) => {
    if (file.mimetype == "application/pdf") {
      cb(null, true);
    } else {
      cb(null, false);
      // return cb(new Error('Only pdf is allowed!'));
    }
  }
});


let arr = []
let namearr = []

app.get("/", (req, res) => {
 res.send('Welscome')
})

app.use(cors());
app.post("/api", uploading.single("file"), (req, res) => {
  res.set(headers)
  if (!req.file) {
    console.log('file error')
    let error = ('Wrong filetype')
    let e = JSON.stringify({error})
    res.json(e)
  }
  let pagesarr = []
  var name = req.file.originalname
  var fileinfo = req.file.path;
  namearr.push(name)
  
  

  setTimeout(() => {

  d = JSON.stringify({fileinfo, pagesarr})
  console.log(d)
  
  res.json(d)
}, 500)

 console.log(arr)
 logger.info(arr)
 
});
app.use(bodyparser.json());


app.post('/csv', (req, res) => {
  res.set(headers)

  let pagesarr = []
  console.log(req.body)
  var fileinfo = req.body.filepath
  var name = req.body.fileselected
  var path = `${name}`
  var pwd = req.body.pdfpwd
  var pwdtru = false
  var csvpath = `./uploads/${name}.csv`
  var csvpath2 = `./uploads/${name}f.csv`
  pdfjs.getDocument({url:fileinfo, password:pwd})
  .promise.then((doc) => {
    var pages = doc._pdfInfo.numPages
    pagesarr.push(pages)
  }).catch((err)=>{console.log(err)
    pwdtru = true
    res.json(err)
    // res.send(err) // wrong password
  })
  // check if csv exists
  fs.exists(csvpath, function(exists) {
    if(exists) {
        console.log('File exists. Deleting now ...');
        fs.unlinkSync(csvpath)
        fs.unlinkSync(csvpath2);
    } else {
        console.log('File not found, so not deleting.');
    }
  });
  
   setTimeout(() => {
    console.log(pwd,pagesarr)
    logger.info(pwd, pagesarr)
    

    // get the first 9 rows 
    const first = new Tabula(fileinfo, {
      area: ["211.68, 33.12, 314.64, 558.72"],
      spreadsheet: true,
      password: pwd,
      pages: '1'
    });
    
    
    // get the rest of page 1 data
    const table = new Tabula(fileinfo, {
      area: ["334.08, 33.12, 711.36, 558.72"],
      spreadsheet: true,
      password: pwd,
      pages: '1'
    });
    
    // get number of pages proper
    var pag = pagesarr[0]
    var r = `2-${pag}`
    
    // get the other pages{filepath}
    const other = new Tabula(fileinfo, {
      area: ["58.32, 33.12, 711.36, 558.72"],
      spreadsheet: true,
      password: pwd,
      pages: r
    });
   

 
      var first9 = first.extractCsv().output
      logger.info(first9)
      var result = table.extractCsv().output
      var otherp = other.extractCsv().output;
  
    setTimeout(() => {
      appendFileSync(`./uploads/${name}f.csv`, first9)
      appendFileSync(`./uploads/${name}.csv`, result)
      appendFileSync(`./uploads/${name}.csv`, otherp)
      if (!pwdtru) {
        var s = ('Success')
        var p = (pwdtru)
        res.json(JSON.stringify({s})
        )
      }
 }, 5000)

 }, 2000)
    
});



app.use(bodyparser.json());
app.post('/data', (req, res) => {
  console.log(req.body)
  let file = req.body.fileselected
  let snddata = []
  res.set(headers)
  
    csv()
    .fromFile(`./uploads/${file}f.csv`)
    .then((data) => {
        snddata.push(data)
    })
  csv()
  .fromFile(`./uploads/${file}.csv`)
  .then((data) => {
      snddata.push(data)
  })
  // csv() // this part right here officer
  // .fromFile(`./uploads/${file}t.csv`)
  // .then((data) => {
  //   final = snddata[1].concat(data)
  //       snddata[1]=final
  // })
  .then(() => {
    res.json(snddata)
  })
  .then(() => {
    fs.unlinkSync(`./uploads/${file}.csv`)
    fs.unlinkSync(`./uploads/${file}f.csv`)
    fs.unlinkSync(`./uploads/${file}`)
  })

})

// const area = {
//     y1: top + "211.68", 334.08 58.32
//     x1: left + "33.12",
//     y2: top + history + "309.6",
//     x2: left +w + "558.72"
// }

app.listen(8000, () => {
  console.log("Server running on 8000");
});
