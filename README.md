RapidDocumentConversion
Group Project by Yasin, Merin, Celestie

In our system the users should be able to upload any WORD document and it will get converted to a PDF document in a single click.​

The purpose of our project is to develop a serverless system using Python and AWS Lambda that can be used to Rapidly convert a WORD document to a PDF format and a system that is user-friendly. Here are the steps that would be done in the backend for the document conversion.​

•User will upload Office Document to S3 bucket.​

•S3 bucket will trigger Lambda function with uploaded files details.​

•Lambda function will convert document.​

•After conversion Lambda function will upload PDF to S3 Bucket.​

Here we have used AWS and Vue as frontend and NodeJs as backend
