const csv = require("csvtojson");

const retrieve = (req, res) => {
    let file = req.body.pdf_name
    let user = req.user
    let snddata = []
    if (user && file) {
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
            .then(() => {
                res.status(200).json(snddata)
            })
    } else {
        res.status(400).json('Not allowed')
    }
}

module.exports = retrieve
