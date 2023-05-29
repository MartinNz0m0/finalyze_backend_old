const bcrypt = require('bcryptjs');
const pool = require('./db');


const register = async (req, resp) =>{
    const salt = await bcrypt.genSalt(10);
    const hash = await bcrypt.hash(req.body.password, salt);
    console.log(req.body)
    const username = req.body.username;
    const master = req.body.masterPassword
    pool.query(`select * from finalyze.users where name='marto'`, async (er, r)=>{
      const isPasswordCorrect = await bcrypt.compareSync(master, r[0].hash);
      if (isPasswordCorrect) {
  
        pool.query(`insert into finalyze.users(name, hash) values('${username}', '${hash}')`, (err, res)=>{
          console.log(res)
          if(err) {
            resp.status(500)
          } else {
            resp.status(200).json("Success")
          }
        })
      }
      else {
        resp.status(503)
      }
    })
}

module.exports = register