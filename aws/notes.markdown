# AWS Notes.

## EC2:

### Instance Types:
**General Purpose:**
- T2: Burstable performance instances.
- M4: Latest generation of general purpose instances.
- M3: Balance of compute, memory and network resources.

**Compute Optimized:**
- C4:
    * Compute optimzied for highest performing processors
    * EBS optimized by default at no additional cost.
    * Support for Enhanced networking and clustering.

- C3:
    * Support for Enhanced networking and clustering.
    * SSd backed instance storage.

**Memory Optimized:**
- X1:
    * Lowest price per GiB of RAM
    * Storage and EBS optimized by default

- R4:
    * Support for Enhanced networking.
    * Memory
 
- R3:
    - SSD Storage
    - Support for Enhanced networking.

**Storage Optimized:**
  - I3:

**Dense Storage Instances:**
  - D2:

**Accelerated Computing Instances:**
  - P2:
  - G2:
  - F1

### Enhanced networking:
* Enhanced Networking: Many instances support enhanced networking. Enhanced networking reduces
  impact of virtualization on network performance by enabling a capability called SR-IOV
  (Single Root I/O virtualization). The result is more PPS, lower latency and less jitter.
* Enhanced neworking is available only for instances launched in Amazon VPC.


### AMIs:
* AMIs define the initial software that will be on an instance when launched.
    - OS
    - Initial state of any patches
    - Application or system software.

* There are 4 sources:
    - Published by AWS
    - The AWS marketplace
    - Generated from existing instances
    - Uploaded virtual servers



### Security Groups:
* Virtual Firewall (Security Groups)

* Security groups have different capabilities depending on whether they are associated
  with an instance in a VPC or Amazon EC2 classic.

EC2 Classic SG - Controls outgoing instance traffic
VPC SG         - Controls outgoing and incoming instance traffic

* SG is stateful firewall; that is an outgoing message is remembered so that the
  response is allowed through the SG without an explicit inbound rule being required.
* Changes to SG are immediate.
* Everything is denied by default. You can add a SG rule to allow traffic, but you cannot
  add a rule to deny traffic.


### Termination protection:
* prevents from accidental termination from console, cli or API.
* It does not prevent termination triggered by an OS shutdown command,
  termination from an autoscaling group or termination of a spot instance due to spot
  price change.


### Pricing options:
**On-Demand instances:** 
- The PPH (price per hour) for each instance type published on AWS website
  represents the price for On-Demand Instances. 
- This is the most flexible pricing option.
  No upfront committment required, and customer has control over when the instance is launched and 
 terminated.
- It is least cost effective of the three pricing options per compute hour


**Reserved Instances:**
- Enables to make capcity reservations for predictable workloads.
- Can save upto 75 percent on the on-demand hourly rate.
- When reserving customers specify instance type and availability zone for the instance
- Capacity in AWS Datacenter is reserved for the customer
- Term commitment and payment option determing the cost of reservation

*payment options:*
  - all upfront: 
  - partial upfront
  - no upfront:

**Modifying your reserved instances**
* Modification does not change the remaining term of your reserved instances. Their end date
  remain the same. There is no fee, and you do not receive a new bill or invoice.
* Modification is different from purchase.

*What can you modify?*:
  * Switch between AZs within the same region.
  * Change between EC2 VPC and EC2 classic.
  * Change the instance type within the same instance family (linux instances only)

* ASG can take advantage of reserved instance pricing. Reserved instances, are a billing construct.
* RI gets applied to any running instance that fits the parameters of the RI. In other words,
  it really isn't associated to just one instance.
* If you have and ASG which launches instances in an AZ where you purchased RI, it will take 
  advantage of that.





### Generic (no suitable location for these notes)

* When launching Windows instance, EC2 generates a random password for the local admin
  account and encrypts the password using public key. Initial access is obtained by
  decrypting the password with the private key, either in the console or using API.
  The decrypted password can be used to login into the instance with local admin account
  via RDP.

* you can only export previously imported EC2 instances. Instances launched within AWS rom AMIs cannot 
  be exported.

* Instance metadata: http://169.254.169.254/latest/meta-data/



---

## S3:



---

## VPC:

