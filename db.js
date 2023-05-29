const {createPool} = require('mysql')
require('dotenv').config();

const pool = createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS, 
    connectionLimit: 10
})

module.exports = pool
