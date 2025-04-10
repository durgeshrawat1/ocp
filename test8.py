{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "apigateway.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:region:account-id:function:your-function-name",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:execute-api:region:account-id:api-id/*"
        }
      }
    }
  ]
}
