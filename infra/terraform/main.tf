# Terraform
terraform {
  required_providers {
    aws = {
      version = ">= 4.0.0"
      source = "hashicorp/aws"
    }
  }
}
# Region
provider "aws" {
  region = "us-west-2"
}
# DynamoDB
resource "aws_dynamodb_table" "prjctVes" {

  name = "prjctVes-DB"
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1
  hash_key = "userID"
  range_key = "ctx"

  attribute {
      name = "userID"
      type = "N"
  }
  attribute {
      name = "ctx"
      type = "S"
  }
}
# Lambda Role
resource "aws_iam_role" "lambda" {
  
  name = "iam-for-lambda-prjctVes"
  assume_role_policy = jsonencode({

    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Sid": "",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        }
      }
    ]
  })
}
# Lambda Policy to allow use of DynamoDB
resource "aws_iam_policy" "lambda-policy-prjctVes" {
  
  name = "lambda_policies_prjctVes"
  
  policy = jsonencode({

    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : ["dynamodb:*"],
        "Resource" : "${aws_dynamodb_table.prjctVes.arn}"
      }
    ]
  })
}
# Lambda Policy Attachment
resource "aws_iam_role_policy_attachment" "attach" {
  
  role = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda-policy-prjctVes.arn

}
# Zip get-steam
data "archive_file" "get-steam" {

  type = "zip"
  source_file = "../../get-steam/main.py"
  output_path = "steam-artifact.zip"

}
# Zip get-stock
data "archive_file" "get-stock" {

  type = "zip"
  source_file = "../../get-stock/main.py"
  output_path = "stock-artifact.zip"

}
# Lambda prjctVes-get-steam
resource "aws_lambda_function" "prjctVes-get-steam" {
  
  role = aws_iam_role.lambda.arn
  function_name = "prjctVes-get-steam"
  handler = "main.lambda_get_steam"
  timeout = 20
  filename = "steam-artifact.zip"
  source_code_hash = data.archive_file.get-steam.output_base64sha256
  runtime = "python3.9"

}
# Lambda prjctVes-get-stock
resource "aws_lambda_function" "prjctVes-get-stock" {
  
  role = aws_iam_role.lambda.arn
  function_name = "prjctVes-get-stock"
  handler = "main.lambda_get_stock"
  timeout = 20
  filename = "stock-artifact.zip"
  source_code_hash = data.archive_file.get-stock.output_base64sha256
  runtime = "python3.9"

}