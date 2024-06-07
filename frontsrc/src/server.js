const express = require('express');
const bodyParser = require('body-parser')
const path = require('path');
const app = express();

const mysql      = require('mysql');
const connection = mysql.createConnection({
  host     : '3.81.8.219',
  user     : 'root',
  password : 'Pri3to.Server',
  database : 'kamailio'
});
connection.connect();

const getSubscriber= async function(user){
  await connection.query(("SELECT * FROM subscriber WHERE username="+user), function (error, results, fields) {
    if (error) throw error;
    console.log('The solution is: ', results);
  });
  return
}

const rates = {US:0.010,DR:0.020}
const updateBalance = async function(){
  await connection.query('SELECT * FROM acc', function (error, results, fields) {
    if (error) throw error;
    console.log('The solution is: ', results);
    
    results.forEach(newLog =>{
      console.log("first char",newLog.dst_user[0])
      switch(newLog.dst_user[0]){
        case '1':
          const newBalance = 3000*rates.US
          const newBal = newBalance.toString()
          connection.query("UPDATE subscriber SET balance="+newBal+" WHERE username="+newLog.src_user, function (error, results, fields) {
          console.log("procesado?",results.message);
        });
          connection.query("DELETE FROM acc WHERE id="+newLog.id, function (error, results, fields) {
          console.log("borrado?",results.message);
        });
        break
      }
    });
    connection.end()
})}
 
updateBalance()
//getSubscriber('102')


app.use(express.static(path.join(__dirname, '../build')));

app.get('/ping', function (req, res) {
 return res.send('pong');
});

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, '../build', 'index.html'));
});

app.listen(process.env.PORT || 80);