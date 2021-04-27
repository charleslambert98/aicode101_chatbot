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
- Currently, the **Course Creation Form** generates the lesson content for a lesson
    - In the image-upload sections, an AWS S3 URL is automatically prepended to the image file name. Since the filesystem has been migrated from S3 to EFS, the prepended URL can be removed as it is all in a "local" filesystem.
    - The course content generated can be directly uploaded to the mounted EFS folder in the appropriate sections (more in the `EFS` directory).

## General Room for Improvement
This section details project-wide improvements that could be made in the event that AWS remains as the framework for the chatbot for an extended period of time.
- Expansion of student interaction with the chatbot
    - General conversation
        - Learning about the chatbot itself
        - Having "human" conversation
- Faster access across AWS services to decrease lag-time between utterance and response
