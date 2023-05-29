const pool = require('./db')
const fs = require('fs')
const csv = require("csvtojson");


const headers = ({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    })

exports.data = (req, res) => {
    console.log(req.body)
    let file = req.body.fileselected
    let user = req.body.user
    let pdfsave = req.body.pdfsave
    let snddata = []
    let date_uploaded = new Date ();
  
    let parts = file.split('_')
    const date = parts[2] + ' - ' + parts[4];
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

    .then(()=>{
      var pdata = JSON.stringify(snddata[0])

      if (user && pdfsave) {
       pool.query(`select * from finalyze.data where name='${user}'`, (err, re) => {
           console.log(re)
        if (re.length != 0) {
          console.log('exists, checking whether data exists')
          pool.query(`select * from finalyze.data where pdf_name='${file}'`, (e, r)=>{

              console.log(r)
              if (r.length != 0) {
                // file exists
              } else {
                pool.query(`INSERT INTO finalyze.data (name, pdf_name, date, date_uploaded, statement_type) VALUES ('${user}', '${file}', '${date}', '${date_uploaded}', 'mpesa')`, (er, r) => {
                    console.log(er, r);
              });
              }
          })
            // exists don't save 
        }
        else if (err) {
          console.log(err)
        }
        else if (re.length==0) {
          console.log('doesnt exist creating new')
           // removed settimeout from here \
            pool.query(`INSERT INTO finalyze.data (name, pdf_name, piedata, date, date_uploaded) VALUES ('${user}', '${file}', '${pdata}','${date}', '${date_uploaded}')`, (er, r) => {
              console.log(er, r);
            });
  
          
        }
       })
      }
    })
    .then(() => {
      res.json(snddata)
    })
    .then(() => {
      if (user && pdfsave) {
        console.log('saving sttdata')
      } else {
      fs.unlinkSync(`./uploads/${file}.csv`)
      fs.unlinkSync(`./uploads/${file}f.csv`)
      }
      fs.unlinkSync(`./uploads/${file}`)
    })
  
}

exports.convert = (req, res) => {
  res.set(headers)

  let pagesarr = []
  var fileinfo = req.body.filepath
  var name = req.body.fileselected
  var path = `${name}`
  var pwd = req.body.pdfpwd
  let user = req.body.user
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
  if (user) {
    // check if the csv exists, notify user csv exists
    fs.exists(csvpath, function(exists) {
      if (exists) {
      res.status(500).json('File exists, please delete the file first')
  } else {
    // do nothing
  }

})
  } else {
    // delete existing csv
  fs.exists(csvpath, function(exists) {
    if(exists) {
        console.log('File exists. Deleting now ...');
        fs.unlinkSync(csvpath)
        fs.unlinkSync(csvpath2);
    } else {
        console.log('File not found, so not deleting.');
    }
  });
}
  
   setTimeout(() => {
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
 }, 3000)

 }, 2000)
    
}
