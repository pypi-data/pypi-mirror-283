import time
import boto3
from botocore.exceptions import ClientError

class StepfunctionsManager:
    def __init__(self, 
                 statemachine_arn: str, 
                 payload: str = None,
                 execution_arn: str = None,
                 max_attempts: int = 10, delay: int = 10,
                 region: str = 'eu-west-1', profile: str = 'default'):
        """
        Initialize the StepfunctionManager instance.

        Args:
            statemachine_arn (str): The Amazon Resource Name (ARN) of the state machine to execute.
            payload (str, optional): The string that contains the JSON input data for the execution. 
                                     Default is None. Example: "payload": "{\"first_name\" : \"test\"}".
            execution_arn (str, optional): The Amazon Resource Name (ARN) of the execution to describe.
                                           Default is None.
            max_attempts (int, optional): Maximum number of attempts to check the execution status. Default is 10.
            delay (int, optional): Delay in seconds between status checks. Default is 10 seconds.
            region (str, optional): AWS region. Defaults to 'eu-west-1'.
            profile (str, optional): AWS profile name. Defaults to 'default'.
        """
        self.statemachine_arn = statemachine_arn
        self.payload = payload if payload is not None else '{}'
        self.execution_arn = execution_arn
        self.max_attempts = max_attempts
        self.delay = delay
        self.region = region
        self.profile = profile

        session = boto3.Session(profile_name=self.profile, region_name=self.region)
        self.sfn_client = session.client('stepfunctions')

    def start_execution(self) -> dict:
        """
        Starts the execution of the specified state machine.

        Returns:
            dict: A dictionary containing the status code and status message.
        """
        try:
            # Start the execution of the state machine with the provided ARN and input payload
            response = self.sfn_client.start_execution(
                stateMachineArn=self.statemachine_arn,
                input=self.payload,
            )

            # Check if the response contains 'executionArn' and 'startDate'
            if 'executionArn' in response and 'startDate' in response:
                return {
                    'statusCode': 200,
                    'statusMessage': f"Stepfunction '{self.statemachine_arn}' started successfully.",
                    'executionArn': response['executionArn']
                }
            else:
                return {
                    'statusCode': 400,
                    'statusMessage': "Failed to start the Stepfunction. No 'executionArn' or 'startDate' in response."
                }

        except ClientError as e:
            return {
                'statusCode': 400,
                'statusMessage': f"AWS Stepfunctions ClientError: {e}"
            }

        except Exception as e:
            # Handle any unexpected errors
            return {
                'statusCode': 400,
                'statusMessage': f"An unexpected error occurred: {e}"
            }

    def describe_execution(self) -> dict:
        """
        Describes the status of the specified execution.

        This method checks the execution status in a loop until it either succeeds,
        fails, or reaches the maximum number of attempts.

        Returns:
            dict: A dictionary containing the status code and status message.
        """
        attempts = 0
        while attempts < self.max_attempts:
            time.sleep(self.delay)
            
            try:
                response = self.sfn_client.describe_execution(
                    executionArn=self.execution_arn
                )

                sfn_state = response['status']

                if sfn_state == 'SUCCEEDED':
                    return {
                        'statusCode': 200,
                        'statusMessage': f"Stepfunction {self.statemachine_arn} completed successfully."
                    }
                elif sfn_state in ['TIMED_OUT', 'FAILED', 'ABORTED', 'PENDING_REDRIVE']:
                    return {
                        'statusCode': 400,
                        'statusMessage': f"Stepfunction {self.statemachine_arn} failed with status: {sfn_state}."
                    }
                
                attempts += 1
            except ClientError as e:
                return {
                    'statusCode': 400,
                    'statusMessage': f"AWS Stepfunctions ClientError: {e}"
                }

            except Exception as e:
                # Handle any unexpected errors
                return {
                    'statusCode': 400,
                    'statusMessage': f"An unexpected error occurred: {e}"
                }
        
        # Return a message if max attempts were reached without successful completion
        return {
            'statusCode': 400,
            'statusMessage': f"Max attempts '{self.max_attempts}' reached for checking stepfunction {self.statemachine_arn} status."
        }
