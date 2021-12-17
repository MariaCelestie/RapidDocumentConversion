const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const dotenv = require('dotenv')
const aws = require('aws-sdk')
const multer = require('multer')
const multerS3 = require('multer-s3')

dotenv.config()
const app = express()

//middleWare
app.use(bodyParser.json())
app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cors())

aws.config.update({
  apiVersion: "2006-03-01",
  accessKeyId: process.env.AWSAccessKeyId,
  secretAccessKey: process.env.AWSSecretKey,
  region: process.env.AWSRegion
})



//Local storage
// var upload = multer({
//   dest: 'upload/'
// });

//S3 storage
const s3 = new aws.S3()
const upload = multer({
  storage: multerS3({
    s3: s3,
    bucket: process.env.AWSBucket,
    acl: "public-read",
    contentType: multerS3.DEFAULT_CONTENT_TYPE,
    metadata: (req, file, cb) => {
      cb(null, { fieldName: file.fieldname})
    },
    key: (req, file, cb) => {
      cb(null, file.originalname)
    }
  })
})


app.get('/', async (req, res) => {
  res.status(200).send('S3 Upload Backend')
})
app.post('/upload', upload.any(), function (req, res, next) {
  try {

    originalName = req.files[0].originalname.split('.')
    originalName = originalName[0]
    console.log(originalName)


    res.status(200).send(originalName)
    
  }
  catch (err) {
    res.status(500).send({
      error: 'error occured uploading file'
    })
  }})

app.post('/', async (err, req, res, next) => {
  
})

const port = process.env.PORT || 5000
app.listen(port, () => {
console.log(`server started on port ${port}`)
});