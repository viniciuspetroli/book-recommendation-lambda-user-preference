data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "dynamodb_access" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:ListTables",
      "dynamodb:DescribeTable",
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem"
    ]

    resources = [
      "arn:aws:dynamodb:sa-east-1:*:table/Users",
      "arn:aws:dynamodb:sa-east-1:*:table/Books",
      "arn:aws:dynamodb:sa-east-1:*:table/Recommendations"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name   = "lambda_dynamodb_policy"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.dynamodb_access.json
}

data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "app"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "LambdaUserPreference"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  runtime = "python3.11"

  environment {
    variables = {
      foo        = "bar",
      secretName = "SecretTest"
    }
  }
}