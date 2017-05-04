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


**Spot instances:**
* Can be used for workloads that are not time critical and are tolerant to interruptions.
* Offer greatest discount
* Specify the price you are willing to pay for a certain instance type. When the bid
  price is above the current spot price, the customer will receive the requested instance.
* These instances operate like all other instances, and customers only pay the spot price for
  the hours the instances run.
* The instances run until:
    * The customers terminate them
    * The spot price goes above the customers bid price
    * There is not enough unused capacity to meet the demand of the spot instances

* If AWS EC2 needs to terminate the spot instance, the instance will receive a termination notice
  providing 2 minute warning prior to terminating the instance.
* If AWS terminates your spot instance, you get the hour it was terminated in for free.
* If you terminate your spot instance, you pay for the hour.


### Tenancy Options:
**Shared Tenancy:**
* Default tenancy model for all EC2 instances regardless of the instance type or pricing.
* Means single host machine may house instances for different customers.
* AWS does not use overprovisioning. Fully isolates instances from other instances on
  the same host.

**Dedicated Instances:**
* Run on hardware that is dedicated to a single customer.
* Other instances in the account will run on shared tenancy and will be isolated at
  hardware level from dedicated instances in the account.

**Dedicated Host:**
* A physical server with EC2 instance capacity fully dedicated to a single customer.
* Customer has control over which specific host runs an instance at launch.

### Placement Groups:
* Is a logical grouping of instances within a single AZ.
* Recommended for applications that benefit from low network latency, high n/w throughput
  or both.



### Instance Stores:
* Provides temporary block-level storage for your instance.
* Size and type of instance store depends on the instance type.
* Data in instance store is lost when:
    * Underlying disk drive fails
    * The instance is stopped
    * The instance is terminated
* Low durability, high IOPS storage





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

## EBS:

* Provides persistent block-level storage volumes for use with EC2 instances.
* Each EBS volume is automatically replicated within it's AZ to provide HA and
  durability.

**Types for EBS Volumes:**

* Magnetic Volumes:
    * Have the lowest performance characteristics
    * Lowest cost per gigabyte
    * Great cost effective solution for appropriate workloads
    * Can range from 1 GB to 1TB and average 100 IOPS, with ability to burst to hunders
      of IOPS.
    * Suited for:
        * Data accessed infrequently
        * Sequential reads
        * Situation where low cost storage is requirement.
    * Billed based on provisioned space, regardless of how much data is actually stored
      on the volume

* General purpose SSD:
    * Strong performance at moderate price
    * Range from 1 GB to 16TB and provides baseline performance of 3 IOPS per Gigabyte provisioned,
      capping at 10,000 IOPS.
      E.G: For a 1 TB volume, you can expect a baseline performance of 3000 IOPS
    * Under 1 TB, it has the ability to burst upto 3000 IOPS for extended periods of time.
    * When not using, IOPS are accumulated as I/O credits, which get used during heavy traffic.
    * Suited for:
        * System boot volumes
        * Small to medium sized DB
        * Development and test environments.

* Provisioned IOPS SSD:
    * Designed to meed needs of I/O intensive workloads
    * Range from 4GB to 16 TB size.
    * When provisioning specify the size and the desired IOPS, upto the lower of 
      (maximum of 30 times the number of GB of volume or 20,000 IOPS)
    * EBS delivers within 10% of the provisioned IOPS 99.9 percent of the time over a given year.
    * Price is on provisioned size.
    * Additional monthly fee is based on provisioned IOPS (whether you consume it or not)
    * Used for:
        * Critical business applications requiring sustained IOPS performance
        * Large DB workloads

* HDD throughput optimized (ST1):
    * Sequential writes
    * Frequently accessed workloads
    * Usually used for data warehouse applications.

* HDD Cold (SC1)
    * Less frequently accessed data
    * Usually used for file servers.

* Note that SC1 and ST1 cannot be used as **Root** volumes.
* HDD, magmetic - standard however can be used as **Root** volume.
* Termination protection is turned off by default, you must turn it on.
* Default action for the root EBS volume is to be deleted when the instance is terminated.


### Protecting Data:
* Snaphots are incremental backups, meaning that only the blocks on the device that have
  changed since your most recent snapshot are saved.
* Snapshots are saved in S3
* The action for taking a snapshot is free. You pay for the storage cost.
* Snapshots are constrained to the region in which they are created. Meaning you can use
  them to create new volumes only in the same region.
* If you need to restore a snapshot in a different region, you can copy a snapshot to
  another region.
* To use a snapshot you create a new EBS volume from the snapshot.
* The volume is created immediately, but data is loaded lazily.
* Means the volume can be accessed upon creation, and if data being requested is not yet
  restored, it will be restored upon first request.
* Snapshots can be used to increase the size of an EBS volume
* Snapshots of encrypted volumes are encrypted automatically.
* Volumes restored from encrypted snaphosts are also encrypted automatically.
* You can share snapshots, but only if they are unencrypted.
* To create a snaphost for EBS volumes that serve as root device, you should stop
  the instance before taking the snapshot.

### Encryption:
* EBS volumes can be encrypted. Uses AWS key management service to handle key management.
* A new master key is created unless you select a master key
* Data and keys are encrypted using AES-256 algorithm.
* Encryption happens on the servers that host the EC2 instance, so the data is actually
  encrypted in transit between the hsot and the storage media and also on the media.
* Encryption is transparent and you can expect same IOPS performance with minimal
  effect on latency.
* Snapshots from encrypted volumes are automatically encrypted as are the volumes created from
  encrypted snapshots.
* EBS root volumes of your default AMIs cannot be encrypted.
* You can use third party tools to encrypt the root volume, or it can be done when creating AMIs in
  the AWS console or using the API.
* You are not tied to the type of volume with snapshot. What it means is you could have a 
  snapshot of a volume of type magnetic disk, and you can create a new volume from this snapshot
  with a different volume type like SSD.



---

## S3:



---

## VPC:

