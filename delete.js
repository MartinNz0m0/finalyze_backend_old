const fs = require('fs')
const pool = require('./db')

const headers = ({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    })

const del = (req, res, next) => {
    // db query to delete the file
    let file = req.body.pdf_name
    let user = req.user
    res.set(headers)
    console.log(req.body, user)
    if (user && file) {
        pool.query(`delete from finalyze.data where pdf_name='${file}' and name='${user}'`, (e, r) => {
            if (e) {
                
                res.status(500).json(e)
            }
            else {
                // check if file exists
                if (!fs.existsSync(`./uploads/${file}.csv`)) {
                    // do nothing
                }
                else {
                fs.unlinkSync(`./uploads/${file}.csv`)
                }
                try {    
                    fs.unlinkSync(`./uploads/${file}f.csv`)
                } catch (error) {
                    console.log(error)
                }
                res.status(200).json('deleted')
            }
        })
    }

}

module.exports = del