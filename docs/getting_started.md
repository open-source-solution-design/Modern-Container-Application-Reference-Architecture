


#  create ssh key pair

```
ssh-keygen
```

# init infra project

pulumi stack init dev
```
cat ~/.ssh/id_rsa.pub | pulumi config set aws:SSH_PUBLIC_KEY
cat ~/.ssh/id_rsa | pulumi config set --secret aws:SSH_PRIATE_KEY
```
