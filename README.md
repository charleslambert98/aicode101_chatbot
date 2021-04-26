# AICode101 Chatbot
Documentation for the AICode101 chatbot, generated using AWS Lambda/Lex/EC2/EFS services.

## Navigating this Repository
This repository contains the appropriate documentation relating to all AWS services used in the project. Inside of each directory is contained another README file that is designed to provide an explanation of the service usage as well as how it can be implemented.

1. **Lambda:** Contains all code handling user requests made to the Lex chatbot
2. **EC2:**  Contains information about EC2 instantiation as well as mounting instruction
3. **EFS:** Contains all files appropriate for usage with Lambda
4. **Lex:** Contains the JSON dump/configuration for the bot

## General Information
Below are general notes or key points that do not fit in a single category but are of importance.

- With regard to the EC2/EFS setup, setting up the EFS **first** will allow for automatic security group generation and mounting to the EC2 instance during instance setup.
- Make sure to have an access point created in the EFS for access to the filesystem from Lambda
- Be sure to have the access point mounted and setup in Lambda before adding any files to the EFS (via EC2). This will ensure the file location is correct and Lambda reads the location as its "root" location (otherwise environment variables will need to be set and configured to navigate to the appropriate directory).
