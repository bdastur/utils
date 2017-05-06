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

### Types for EBS Volumes:

#### Magnetic Volumes:
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

#### General purpose SSD:
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

#### Provisioned IOPS SSD:
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

#### HDD throughput optimized (ST1):
    * Sequential writes
    * Frequently accessed workloads
    * Usually used for data warehouse applications.

#### HDD Cold (SC1)
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

## EFS:
* Supports the Network File System version 4 (NFSv4) protocol
* You only pay for the storage you use
* Can scale up to petabytes
* Can support thousands of concurrent NFS connections
* Data is stored across multiple AZs within a region
* Read after write consistency.
* Great use case for a file server



---

## ELB:

* ELB service allows you to distribute traffic across a group of EC2 instances in
  one or more availability zones within a region.

* Internet facing ELB:
    * A load balancer that takes requests from clients over the internet and 
      distributes them to EC2 instances registered with the ELB.
    * It receives public DNS name that clients can use to send requests to your
      application.

* Internal ELB
    * As the name suggest is not exposed to clients on the web.

* ELB in VPCs support IPV4 addresses only, ELB in EC2 classic supports IPV4 and IPV6.

* HTTPS load balancers:
    * Uses SSL/TLS protocol for encrypted connections.
    * Enables encryption between clients and the ELB.
    * Must install SSL Cert on the ELB.
    * ELB does not support **Server Name Indication** (SNI). This means if you want
      to host multiple websites on a fleet of EC2 instances behind ELB with a single
      SSL, you will naeed to add **Subject Alternative Name** for each website to the
      certificate to avoid site users seeing a warning message when the site is
      accessed.

* Listener is a process that checks for connection requests
* Listener is configured with a protocol and a prot for the front end and back end connection.
* Protocols: HTTP, HTTPS, SSL, TCP
* Protocols operate at layer 4 and layer 7

* Idle connection timeout:
    * For each request a client makes, the ELB maintains 2 connections.
    * For each connection the ELB manages the idle timeout and is triggered when no
      data is sent over the connection for the specified time period.
    * After the timeout period, the ELB closes the connection.
    * Default idle timeout is 60 seconds for both connections.
    * If using HTTP or HTTPS, recommendation is to use the keep-alive option for EC2
      instances.
    * You can enable keepalive in the web server settings or kernel settings of EC2
      instance.
    * Keepalive enablees ELB to reuse connections to your backend instance, which reduces
      CPU utilization.
    * To ensure that ELB is responsible for closing the connections to the instance,
      make sure that the keepalive time is greater than the idel timeout setting on
      the ELB.

* Cross zone load balancing ensures that request traffic is routed evenly across
  all backend instances regardless of AZ.

* Connection Draining:
    * ensures that ELB stops sending requests to instances that are deregistered or
      unhealthy, while keeping existing connections open.
    * Enables ELB to complete inflight requests made to these instances.
    * Max timeout value between 1 and 3600 seconds. Default is 300 seconds.

* Proxy Protocol:
    * Allows ELB to add a human readable header with connection information such as source
      IP addr, dest ip and port numbers. Header is sent to backend instance as part of
      the request.
    * Ensure that the ELB is not sitting behind a proxy server with proxy protocol enabled,
      otherwise there will be a duplicate header.

* Sticky Sessions:
    * Enables ELB to bind a users session to a specific instance. This ensures that
      all requests from the user during the session are sent to the same instance.
    * Key to managing sticky sessions is to determinte how long your ELB should 
      consistently route the user requests to the same instance.
    * If your app has a session cookie, configure the ELB so that the session cookie follows
      the duration specified by the applications session cookie
    * You can configure ELB to create a session cookie by specifying your own stickiness
      duration. ELB creates a cookie named AWSELB that is used to map the session to the instance.

* Health checks:
    * To test the status of the EC2 instance behind the ELB
    * Either InService or OutofService



---

## Autoscaling:

* Allows automatic scaling of EC2 instances based on a criteria.
* Scaling in or scaling out.

**Autoscaling Plans:**

* Maintain current levels:
    * Maintain a minimum number of running instances at all times
    * When ASG finds an unhealthy instance it terminates it and launches a new one.
* Manual scaling:
    * You only need to specify the change in max, min or desired capacity of your ASG group.
    * ASG maintains the process of creating or terminating instances to maintain the updated capacity.
* Scheduled scaling:
    * by schedule
* Dynamic scaling:
    * Create a scaling policy based on criteria like n/w bandwidth or CPU measured by cloudwatch
      and measure a threshold.


**ASG Components**

* Launch Configuration:
    * A template that ASG uses to create new instances.
    * It is composed of config name, AMI, instance type, SG key pair.
    * Default limit of launch config is 100 per region.
    * Only a launch config name, AMI and instance type are needed to create a launch config.
      key pair, SG and block device mapping are optional elements.

* Autoscaling Group:
    * Is a collection of EC2 instances managed by ASG service.
    * Each ASG contains config options that control when auto scaling should launch new
      instances and terminate existing ones. You specify the max, min and desired capacity.
    * ASG can use on-demand or spot instances as EC2 instances it manages.
    * On-demand is default, but spot instances can be used by referencing a max bid price in
      the launch config.
   * A launch config can reference on-demand or spot instances but not both.

* Scaling Policy
    * You can associate cloudwatch alarms and scaling policies to an ASG group to 
      adjust dynamically.
    * The policy is a set of instructions that tell ASG whether to scale out or scale in.
    * You can associate more than on scaling policy to an ASG group.

* You are billed for a full hour of running time even for EC2 instances that are launched
  and terminated within the hour.
* A good ASG best practice is to scale out quickly when needed but to scale in more slowly
  to avoid having to relaunch new and separate EC2 instances for a spike in workload
  that fluctuates up and down within minutes.
* It is important to consider bootstrapping for EC2 instances launched by ASG.
* It takes time to configure each new EC2 instance before the instance is healthy and 
  capable of accepting traffic. Instances that start and are available to load faster can join
  the capacity pool more quickly.
* Instances that are more stateless instead of stateful will more gracefully enter and
  exit an ASG group.



---

## S3:

### S3 Read-after-write consistency:
* S3 provides read-after-write consistency for PUTS to new objects (new key), but
  eventual consistency for GETs and DELETEs of existing objects (existing key).
  Eventual consistency means if you PUT new data to an existing key, a subsequent
  GET might return old data. Similarly if you DELETE an object, a subsequent GET
  for that object might still read the deleted object.
  In all cases updates to a single key are atomic - for eventually-consistent reads
  you will get new data or old data, but never an inconsistent mix of data.

* Durability in S3 is achieved by replicating data geographically to different AZz
  regardless of the versioning configuration. AWS does not use tables.
* Bucket names must be unique across all AWS accounts, much like DNS names.
* Bucket names can contain upto 63 lowercase letters, numbers, hyphens and periods.
* You can have upto 100 buckets per account by default.
* Even though the namespace for S3 is global, each S3 bucket is created in a specific
  region that you choose. This let's you control where the data is stored.
* Each object consist of data and metadata. Data is opaque to S3. Data is treated
  simply as a stream of bytes.
* Metadata can be system metadata: created and used by Amazon S3 or user metadata
  which is optional and can only be specified during object creation time
* Keys define the objects in S3 buckets. It can be upto 1024 bytes of unicode UTF-8
  characters, including embedded slashes, backslashes, dots and dashes.

**Bucket Url:**

* S3 website URL:   https://bucketname.s3-website.us-east-1.amazon.aws.com
* Normal bucket URL: https://s3.amazonaws.com/(bucketname)/(keypath)
* Object URL: https://bucketname.s3.amazonaws.com/path/to/my/file.ext

* S3 has durability of 99.999999999% and Availability of 99.9%
* You can use the PUT api to put an object into S3. Largest object size can be 5GB. After that
  you have to use multipart upload.
* For objects larger than 100 MB you should infact use multipart upload.
* Minimum file size can be 0 bytes

* RSS: Reduced Redundancy storage. RSS offers 99.9% durability.

### Access Control:
* By default when you create a bucket or object in S3, only you have access.
* To allow access to others S3 provides ACLs (coarse grained access controls)
  or IAM policies which are much finer grained.
* ACLs allow you to grant certain coarse-grained permissions: Read, Write and Full control
  on the object or bucket. ACLs are legacy access control created before IAM existed.
* S3 bucket policies are the recommended access control mechanism for S3 and provide
  much finer-grained control.

### Static website hosting:
* Create a bucket, upload static files, make them public (world readable)
* Enable static website hosting for the bcuket. This includes specifying an index
  document and an error document.
* The website will be available at https://<bucketname>.s3-website>-<aws region>.amazonaws.com
* You can create a friendly DNS name in your own domain for the website using a CNAME and 
  you have your website available.


### Storage classes:

**S3 Standard:**
* High durability, high availability, low latency and high performance object store
  for general purpose use.
* Offers low first-byte latency and high throughput.

**S3 Standard - Infrequent Access:**
* High/same durability, low latency and high throughput as S3 standard, but is designed
  for long-lived, less frequently accessed data.
* It has lower per GB-month storage cost than standard.
* Minimum object size of 128KB
* Minimum duration of 30 days and per-GB retrieval costs.

**S3 Reduced Redundancy Storage (RRS):**
* Offers slightly less durability (4 nines) than standard or standard IA at reduced cost.

**Amazon Glacier:**
* Secure, durable and extremely low cost storage for data
* Optimized for infrequently accessed data.
* To retrieve object from glacier you issue a restore command using S3 APIs. Three to five 
  hours later object is copied to S3 RRS.
* Glacier allows you to retrieve upto 5% of the S3 data store in Glacier for free each month.
* Glacier is not currently available in Asia Pacific (Singapore) and South America (Sao Paulo)
* Designed for data that is retained for more than 90 days. 
* Objects archived to Glacier incur cost for atleast 90 days enen if they are deleted or 
  overwritten earlier.

### Versioning:
* Versioning is enabled at the bucket level.
* Once turned on versioning cannot be removed from the bucket, it can only be suspended.

### MFA Delete:
* Requires additional authentication to delete an object version or change
  the versioning state of a bucket.
* MFA delete requires an additional authentication code generated by a hardware or MFA device.
* MFA delete can only be enabled by root account.

### Presigned URLs:
* All S3 objects are by default private. However object owner can optionally share objects
  with others by creating a pre-signed URL, using their own security credentials to grant
  time-limited permissions to download the objects.
* To create a pre-signed URL for object, you must provide your security credentials,
  specify the bucket, the object key, the HTTP method and an expiration date and time.
* The pre-signed URLS are valid only for specific time.

Example of creating a presigned URL:
```
>>> import boto3
>>> session = boto3.Session(profile_name="production", region_name="us-east-1")
>>> s3client = session.client('s3')
>>> s3client.generate_presigned_url('get_object', 
                                    Params={'Bucket': 'mysample-s3-bucket', 'Key': 'scripts/aws_volume_helper.py'}, 
                                    ExpiresIn=3600)
u'https://mysample-s3-bucket.s3.amazonaws.com/scripts/aws_volume_helper.py?AWSAccessKeyId=AXIXXXX6FXXXXEXXXX&Expires=1491340796&Signature=2pfqmdtyOcRbXWQ8'
>>>
```

### Multipart Uploads:
* todo


### Cross-Region Replication:
* To enable cross-region replicatio versioning must be enabled on source and destination
  bucket.
* Only new data will be replicated, existing data must be copied over.
* Any metadata and ACLs associated with the objects are also part of the replication.
* When you delete specific versions of an object or delete a delete marker, it does
  not get replicated to the target bucket. It's only when you delete an object that it
  gets deleted from the replicated bucket.

### S3 Request Rate and Performance considerations:
* S3 will scale automatically to support very high request rates, automatically
  re-partitioning your buckets as needed. 
* If you need request rates higher than 100 requests/second, you may want to review
  the S3 best practices guidelines in DEV guide.
* To support higher request rates, it is best to ensure some level of random distribution of
  keys. For eg. including a hash as a prefix to key names.

http://docs.aws.amazon.com/AmazonS3/latest/dev/request-rate-perf-considerations.html

### S3 Charges:
* You are charged for:
    * Storage
    * Requests
    * Storage management pricing (you can add tags to objects, buckets - charged for each tag)
    * Data transfer pricing
    * Transfer acceleration


### S3 Transfer Acceleration:
* Enables fast, easy and secure transfer of files over long distances
  between client and an S3 bucket.
* Transfer acceleration takes advantage of CloudFront's globally distributed edge locations.
* As data arrives at an edge location, data is routed to Amazon S3 over an optimized networ path.
* Additional charges may apply.













---

## VPC:































