const pool = require('./db');

const dash = (req, res) => {
    let user = req.user
    console.log(user)
    pool.query(`select * from finalyze.data where name='${user}'`, (e, r)=> {
        let jibu = r
        if (e) {
            res.status(500).json(e)
        } else {

            res.status(200).json(jibu)
        }
    })
}

module.exports = dash