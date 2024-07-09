# Table of Contents

* [aws](#aws)
* [aws.lambda\_functions](#aws.lambda_functions)
  * [LambdaManager](#aws.lambda_functions.LambdaManager)
    * [\_\_init\_\_](#aws.lambda_functions.LambdaManager.__init__)
    * [invoke\_lambda](#aws.lambda_functions.LambdaManager.invoke_lambda)
* [aws.glue](#aws.glue)
  * [GlueManager](#aws.glue.GlueManager)
    * [\_\_init\_\_](#aws.glue.GlueManager.__init__)
    * [check\_crawler\_status](#aws.glue.GlueManager.check_crawler_status)
* [aws.stepfunctions](#aws.stepfunctions)
  * [StepfunctionsManager](#aws.stepfunctions.StepfunctionsManager)
    * [\_\_init\_\_](#aws.stepfunctions.StepfunctionsManager.__init__)
    * [start\_execution](#aws.stepfunctions.StepfunctionsManager.start_execution)
    * [describe\_execution](#aws.stepfunctions.StepfunctionsManager.describe_execution)
* [aws.cloudwatch](#aws.cloudwatch)
  * [CWManager](#aws.cloudwatch.CWManager)
    * [\_\_init\_\_](#aws.cloudwatch.CWManager.__init__)
    * [check\_cloudwatch\_alarm\_state](#aws.cloudwatch.CWManager.check_cloudwatch_alarm_state)
* [aws.s3](#aws.s3)
  * [S3Manager](#aws.s3.S3Manager)
    * [\_\_init\_\_](#aws.s3.S3Manager.__init__)
    * [upload\_file](#aws.s3.S3Manager.upload_file)
    * [check\_file\_exists](#aws.s3.S3Manager.check_file_exists)

<a id="aws"></a>

# aws

<a id="aws.lambda_functions"></a>

# aws.lambda\_functions

<a id="aws.lambda_functions.LambdaManager"></a>

## LambdaManager Objects

```python
class LambdaManager()
```

<a id="aws.lambda_functions.LambdaManager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(lambda_name: str,
             payload: dict = None,
             region: str = 'eu-west-1',
             profile: str = 'default')
```

Initialize the LambdaManager instance.

**Arguments**:

- `lambda_name` _str_ - The name of the AWS Lambda function.
- `payload` _dict, optional_ - The payload to be sent to the Lambda function.
  Default is None. Example: payload = '{ "key": "value" }'
- `region` _str, optional_ - AWS region. Defaults to 'eu-west-1'.
- `profile` _str, optional_ - AWS profile name. Defaults to 'default'.

<a id="aws.lambda_functions.LambdaManager.invoke_lambda"></a>

#### invoke\_lambda

```python
def invoke_lambda() -> dict
```

Invoke the AWS Lambda function synchronously and return the status of the invocation.

**Returns**:

- `dict` - A dictionary containing the status code and status message.
  - 'statusCode' (int): HTTP status code indicating the result of the invocation.
  - 'statusMessage' (str): Status message describing the outcome of the invocation.

<a id="aws.glue"></a>

# aws.glue

<a id="aws.glue.GlueManager"></a>

## GlueManager Objects

```python
class GlueManager()
```

<a id="aws.glue.GlueManager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(crawler_name: str,
             max_attempts: int = 10,
             delay: int = 30,
             region: str = 'eu-west-1',
             profile: str = 'default')
```

Initialize a GlueManager instance to manage AWS Glue crawlers.

**Arguments**:

- `crawler_name` _str_ - The name of the AWS Glue crawler.
- `max_attempts` _int, optional_ - Maximum number of attempts to check the crawler status. Default is 10.
- `delay` _int, optional_ - Delay in seconds between status checks. Default is 30 seconds.
- `region` _str, optional_ - AWS region. Defaults to 'eu-west-1'.
- `profile` _str, optional_ - AWS profile name. Defaults to 'default'.

<a id="aws.glue.GlueManager.check_crawler_status"></a>

#### check\_crawler\_status

```python
def check_crawler_status() -> dict
```

Checks the status of an AWS Glue crawler.

**Returns**:

- `dict` - A dictionary containing the status code and status message.

<a id="aws.stepfunctions"></a>

# aws.stepfunctions

<a id="aws.stepfunctions.StepfunctionsManager"></a>

## StepfunctionsManager Objects

```python
class StepfunctionsManager()
```

<a id="aws.stepfunctions.StepfunctionsManager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(statemachine_arn: str,
             payload: str = None,
             execution_arn: str = None,
             max_attempts: int = 10,
             delay: int = 10,
             region: str = 'eu-west-1',
             profile: str = 'default')
```

Initialize the StepfunctionManager instance.

**Arguments**:

- `statemachine_arn` _str_ - The Amazon Resource Name (ARN) of the state machine to execute.
- `payload` _str, optional_ - The string that contains the JSON input data for the execution.
  Default is None. Example: "payload": "{"first_name" : "test"}".
- `execution_arn` _str, optional_ - The Amazon Resource Name (ARN) of the execution to describe.
  Default is None.
- `max_attempts` _int, optional_ - Maximum number of attempts to check the execution status. Default is 10.
- `delay` _int, optional_ - Delay in seconds between status checks. Default is 10 seconds.
- `region` _str, optional_ - AWS region. Defaults to 'eu-west-1'.
- `profile` _str, optional_ - AWS profile name. Defaults to 'default'.

<a id="aws.stepfunctions.StepfunctionsManager.start_execution"></a>

#### start\_execution

```python
def start_execution() -> dict
```

Starts the execution of the specified state machine.

**Returns**:

- `dict` - A dictionary containing the status code and status message.

<a id="aws.stepfunctions.StepfunctionsManager.describe_execution"></a>

#### describe\_execution

```python
def describe_execution() -> dict
```

Describes the status of the specified execution.

This method checks the execution status in a loop until it either succeeds,
fails, or reaches the maximum number of attempts.

**Returns**:

- `dict` - A dictionary containing the status code and status message.

<a id="aws.cloudwatch"></a>

# aws.cloudwatch

<a id="aws.cloudwatch.CWManager"></a>

## CWManager Objects

```python
class CWManager()
```

<a id="aws.cloudwatch.CWManager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(alarm_name: str,
             start_date: datetime,
             end_date: datetime,
             region: str = 'eu-west-1',
             profile: str = 'default')
```

Initializes the CWManager with the specified alarm name and date range.

**Arguments**:

- `alarm_name` _str_ - The name of the CloudWatch alarm.
- `start_date` _datetime_ - The start date for the alarm history query.
- `end_date` _datetime_ - The end date for the alarm history query.
- `region` _str, optional_ - AWS region. Defaults to 'eu-west-1'.
- `profile` _str, optional_ - AWS profile name. Defaults to 'default'.

<a id="aws.cloudwatch.CWManager.check_cloudwatch_alarm_state"></a>

#### check\_cloudwatch\_alarm\_state

```python
def check_cloudwatch_alarm_state() -> dict
```

Checks the state history of the specified CloudWatch alarm within the given date range.

**Returns**:

- `dict` - A dictionary containing the status code and message indicating whether the alarm state changed to ALARM.

<a id="aws.s3"></a>

# aws.s3

<a id="aws.s3.S3Manager"></a>

## S3Manager Objects

```python
class S3Manager()
```

<a id="aws.s3.S3Manager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(bucket_name: str,
             object_name: str,
             file_name: str = None,
             region: str = 'eu-west-1',
             profile: str = 'default')
```

Initialize an S3Manager instance.

**Arguments**:

- `bucket_name` _str_ - The name of the bucket to upload to.
- `object_name` _str_ - The name of the key to upload to.
- `file_name` _str_ - The path to the file to upload.
- `region` _str, optional_ - AWS region. Defaults to 'eu-west-1'.
- `profile` _str, optional_ - AWS profile name. Defaults to 'default'.

<a id="aws.s3.S3Manager.upload_file"></a>

#### upload\_file

```python
def upload_file() -> dict
```

Upload a file to an S3 bucket.

**Returns**:

- `dict` - A dictionary containing the status code and status message.

<a id="aws.s3.S3Manager.check_file_exists"></a>

#### check\_file\_exists

```python
def check_file_exists() -> dict
```

Check if the specified file exists in the S3 bucket and if it was
modified in the last one minute of UTC time.

**Returns**:

- `dict` - A dictionary containing the status code and status message.

