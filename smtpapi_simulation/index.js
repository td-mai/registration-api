const express = require('express');
const ejs = require('ejs');
const app = express();
const port = 5001;

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const multer = require('multer');
const upload = multer();
app.use(upload.array());

let mails = []

function cleanOldMails() {
    mails = mails.filter(function(mail, index, arr){ 
        return mail.date > new Date(Date.now() - 86400*1000);
    });
}
  
setInterval(cleanOldMails, 360*1000);
  
app.post('/api/sendemail', (req, res) => {

    if (!req.body){
        res.sendStatus(400)
    }
    const sender = req.body.sender
    const receiver = req.body.receiver 
    const text = req.body.text

    if (!sender || !receiver || !text){
        res.sendStatus(400)   
    }else{

        mails.push({
            date: new Date(),
            sender: sender,
            receiver: receiver,
            content: text
        })
        res.sendStatus(200)

    } 
})

app.get('/', (req, res) => {
    res.render("home.ejs", {mails: mails})
});

app.listen(port, () => console.log(`Smtp simulation is listening on port ${port}!`));