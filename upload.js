const pool = require('./db');

const headers = ({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    })


exports.uploadcoop = (req, res) => {
    res.set(headers)
    user = req.user
    let namearr = []

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
    currdate = new Date()
    
    // check all sata for user in db
    pool.query(`select * from finalyze.data where name='${user}'`, (e, r)=> {
      let jibu = r
      if (e) {
          res.status(500).json(e)
      } else {
        // check if the file exists
        let fileexists = false
        console.log(jibu)
        for (let i = 0; i < jibu.length; i++) {
          if (jibu[i].pdf_name == name) {
            fileexists = true
          }}
        if (fileexists) {
          res.status(500).json('File exists, please delete the file first')
        } else {
          // add file to db
          pool.query(`insert into finalyze.data (name, pdf_name, date_uploaded, statement_type) values ('${user}', '${name}', '${currdate}', 'coop')`, (e, r) => {
            if (e) {
              res.status(500).json(e)
            } else {
              // do nothing
             
              res.status(200).json('File uploaded')
            }
          })
        }
      }
    })  
}

// for equity
exports.uploadequity = (req, res) => {
    res.set(headers)
    user = req.user
    let namearr = []

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
    currdate = new Date()

    // check all sata for user in db
    pool.query(`select * from finalyze.data where name='${user}'`, (e, r)=> {
        let jibu = r
        if (e) {
            res.status(500).json(e)
        } else {
            // check if the file exists
            let fileexists = false
            console.log(jibu)
            for (let i = 0; i < jibu.length; i++) {
                if (jibu[i].pdf_name == name) {
                    fileexists = true
                }}
            if (fileexists) {
                res.status(500).json('File exists, please delete the file first')
            } else {
                // add file to db
                pool.query(`insert into finalyze.data (name, pdf_name, date_uploaded, statement_type) values ('${user}', '${name}', '${currdate}', 'equity')`, (e, r) => {
                    if (e) {
                        res.status(500).json(e)
                    } else {
                        // do nothing

                        res.status(200).json('File uploaded')
                    }
                })
            }
        }
    })
}