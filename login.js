const passport = require('passport');
const jwt = require('jsonwebtoken');
require('dotenv').config();


const LocalStrategy = require('passport-local').Strategy;
const headers = ({
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*'
  })

const login = (req, resp, next) => {
    resp.set(headers)
    const username = req.body.username;
    const pass = req.body.password
  
    passport.authenticate('local', {session: false}, (err, username, info) => {
      if (err || !username) {
        console.log(err)
          return resp.status(400).json({
              message: 'Something is not right',
              username   : username
          });
      }       
      req.login(username, {session: false}, (err) => {
         if (err) {
             resp.send(err);
         }           // generate a signed son web token with the contents of username object and return it in the response
         const options = { expiresIn: '1d' };           
         const token = jwt.sign(username, process.env.SECRET, options);
         return resp.json({username, token});
      });
    })(req, resp, next);

   
  }

module.exports = login