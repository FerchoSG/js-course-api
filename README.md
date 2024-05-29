```bash
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-udg4ybr1qt3t
```

```bash
sam deploy  --template-file packaged.yaml --stack-name course-test-api --capabilities CAPABILITY_IAM, CAPABILITY_NAMED_IAM
```

```bash
sam deploy --stack-name course-test-api --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-udg4ybr1qt3t --capabilities CAPABILITY_IAM
```