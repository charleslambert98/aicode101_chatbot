# EFS
The Elastic File System (EFS) is the service we use to provide Lambda with access to the libraries and files needed to perform it's operation. This section will detail the File System structure and its setup.

## EFS Configuration
The file system is simple to create. All that is needed is the name and which VPC you would like to connect it to. There is a configuration option, but that is not necessary unless you wish to add tags or modify specific settings.

## Access Point Configuration
Creating the access point requires slightly more setting up.

1. Select "Create access point"
2. Provide an access point name
3. Select "/efs" as the root directory path
    1. This will define the directory **inside** of the EFS
    2. If you do not include this, the root directory of the EFS will be the access point directory
    3. It is recommended to include a root directory path in the event multiple projects or access points are created on one EC2 instance
4. Under "POSIX user":
    1. **User ID:** 1000
    2. **Group ID:** 1000
    3. **Secondary Group IDs:** Leave Blank
5. Under "Root directory creation permissions":
    1. **Owner User ID:** 1000
    2. **Owner Group ID:** 1000
    3. **Permissions:** 777
        1. These permissions are the same as typical file system permissions. If you wish to limit access, you can modify the permissions.
6. Under "Tags", include any tags that you'd like.
7. Select "Create access point"

## File System Structure
The structure of the file system is relatively straight-forward, and is completely open to modification.

All files need to be included in the mounted file system, specifically in the access point's directory so that Lambda can access it (Lambda does not access the file system, but the access point **in** the file system).

Files included in the system are:
- Python library files: Anything from site-packages that is necessary
- Course content files: Files/folders outlining each lesson available in the chatbot

All files in the EFS have been included in this directory.