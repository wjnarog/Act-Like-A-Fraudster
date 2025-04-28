const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();
const PORT = 3000;

// Main page
router.get('/',function(req,res){
  res.sendFile(path.join(__dirname+'/public/index.html'));
  res.sendFile(path.join(__dirname+'/public/normalize.css'));
  res.sendFile(path.join(__dirname+'/public/style.css'));
  //__dirname : It will resolve to your project folder.
});

// Address page
router.get('/address',function(req,res){
  res.sendFile(path.join(__dirname+'/public/address.html'));
});

// County page
router.get('/county',function(req,res){
  res.sendFile(path.join(__dirname+'/public/county.html'));
});

// CSS Loading
app.use(express.static(__dirname+"/public"))

// Terminal Message
app.listen(PORT, () => {
    console.log(`Node.js server running at http://localhost:${PORT}`);
});