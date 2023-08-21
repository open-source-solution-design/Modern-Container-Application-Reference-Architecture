# Infrastructure as Code (IAC) Project
This project uses Infrastructure as Code (IAC) to manage and observe cloud resources.

# Directory Structure
```
├── iac
│   ├── config
│   ├── input
│   ├── cmdb_inventory
│   ├── state_sync_graph_db
│   ├── output
│   └── state_backend
├── cloud
│   └── providers
│       ├── aliyun
│       ├── azure
│       ├── tencent_cloud
│       ├── gcp
│       └── aws
├── identity_and_access
│   ├── organization
│   ├── role
│   ├── user
│   ├── account
│   └── permission
├── resource
│   ├── IaaS
│       ├── database
│       ├── network
│       ├── storage
│       ├── container
│       └── compute
├── service
│   ├── PaaS
│   │   ├── message
│   │   ├── DB
│   │   ├── cache
│   │   └── event
│   │   ├── kubernetes_engine
│   ├── serverless
│   │   ├── app_engine
│   │   └── cloud_functions
│   └── saas
│       ├── cdn
│       ├── waf
│       ├── sns
│       ├── monitoring

```
# Todo Features

1. Multi-cloud support: The project supports multiple cloud platforms including AWS, GCP, Azure, Aliyun, and Tencent Cloud.
2. Resource/Service Management: It allows for the creation, deletion, modification, and querying of resources/services.
3. Terraform/Pulumi Support: The project supports both Terraform and Pulumi for defining and providing data center infrastructure using code.
4. Cloud CMDB: It includes a Configuration Management Database (CMDB) for storing information about hardware and software assets.
5. Multi-cloud Account Resource Analysis: It supports analysis and observation of resources across multiple cloud accounts.
6. Integration with Other Configuration Tools: The project can be integrated with other configuration tools like Ansible for configuration management.

# Description of Directories

* iac: This directory contains all files related to Infrastructure as Code (IAC). This includes input files, CMDB inventory, state synchronization graph database, output files, and state backend.
* iac/input: This directory stores all the input files, which describe the resources you want to create or manage.
* iac/cmdb_inventory: This directory contains the inventory files for the Cloud Configuration Management Database (CMDB), which are used to track and manage the configuration of cloud resources.
* iac/state_sync_graph_db: This directory contains the state synchronization graph database, which is used to track the state and dependencies of resources.
* iac/output: This directory stores all the output files, which describe the results of IAC operations.
* iac/state_backend: This directory contains the state backend files, which are used to store and track the state of resources.

* account: This directory contains all files related to accounts, such as organization, role, user, user-group, and permissions.
* cloud: This directory contains all files related to cloud, including configuration and providers.
* cloud/config: This directory stores cloud configuration files.
* cloud/providers: This directory contains specific configurations and related files for each cloud provider, such as AWS, GCP, Azure, Alibaba Cloud, and Tencent Cloud.
* resource: This directory contains all files related to various resource types, such as PaaS, IaaS, identity and access management, AWS, and SaaS resources.
* service: This directory contains all files related to services, such as PaaS, serverless, and SaaS services.

