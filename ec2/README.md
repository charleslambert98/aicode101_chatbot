# EC2
This section handles the creation of the EC2 instance as well as ensuring successful mounting of the EFS.

## EC2 Instance Configuration
**WARNING:** If you have not yet created your EFS, it is highly suggested you do that first. When creating the EFS first then creating the EC2 instance, you will have the option to mount and EFS which will automatically generate all necessary security groups and configure all necessary to make it accessible.

1. In the EC2 Dashboard, select "Launch instances"
2. Select "Amazon Linux 2 AMI (HVM), SSD Volume Type" (the x86 version)
3. Choose instance type (the "Free tier eligible" section was selected)
4. Click "Configure Instance Details"
5. Most settings can remain the same, but be mindful of:
    1. **Subnet:** No preference
    2. **File systems:** Select "Add file system" and ensure your EFS is selected
6. Click "Add Storage"
7. Add storage if you'd like 
8. Click "Add Tags"
9. Add tags if you'd like
10. Click "Configure Security Group"
11. It will mention the security protocols being created due to the EFS as well as the default protocol for EC2 access
12. Click "Review and Launch"

**Note:** Be sure to store the .pem file associated with remote access to the EC2 instance via SSH. This is required if you plan on accessing the instance from a local system. You will still be able to access the instance from the dashboard, but SSH/SCP tends to be more convenient.

## Instance Details
- **Platform:** Amazon Linux
    - Linux/UNIX
- **Type:** t2.micro
- **Security Groups:** Pre-defined by VPC (default) and auto-generated on creation by EFS
- **Storage:** 8 GiB 
    - Not important unless you plan on loading onto the EC2 instance itself and not the mounted EFS
    - 8 Gib proved to be enough for all necessary software (python3.8, etc.)

