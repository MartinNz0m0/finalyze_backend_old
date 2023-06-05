const passport = require("passport");
const pool = require("./db");
const bcrypt = require("bcryptjs");
const passportJWT = require("passport-jwt");
const JWTStrategy = passportJWT.Strategy;
const ExtractJWT = passportJWT.ExtractJwt;
require('dotenv').config();

const LocalStrategy = require("passport-local").Strategy;

passport.use(
  new LocalStrategy(
    {
      usernameField: "username",
      passwordField: "password",
    },
    function (username, password, done) {
      const query = "SELECT * FROM finalyze.users WHERE name = ?";
      const values = [username];

      pool.query(query, values, async (err, res) => {
        try {
          console.log(err, res);
          const isPasswordCorrect = await bcrypt.compareSync(
            password,
            res[0].hash
          );
          const username = {
            name: res[0].name,
            role: res[0].role,
          };
          if (err) {
            return done(null, false, { message: "Incorrect credentials" });
          }
          if (!isPasswordCorrect) {
            return done(null, false, { message: "Incorrect credentials" });
          } else {
            return done(null, username, { message: "Logged In Successfully" });
          }
        } catch (error) {
          console.log(error);
        }
      });
    }
  )
);

passport.use(
  new JWTStrategy(
    {
      jwtFromRequest: ExtractJWT.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.SECRET,
    },
    function (jwtPayload, cb) {
      //find the user in db if needed. This functionality may be omitted if you store everything you'll need in JWT payload.
      console.log(jwtPayload);
      return pool.query(
        `select * from finalyze.users where name='${jwtPayload.name}'`,
        (err, res) => {
          if (err) {
            console.log(err);
            return cb(err);
          }
          return cb(null, res[0].name);
        }
      );
    }
  )
);
