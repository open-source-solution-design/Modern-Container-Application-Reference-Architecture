


#  create ssh key pair

```
ssh-keygen
```

# init infra project

pulumi stack init dev --secrets-provider passphrase
```
cat ~/.ssh/id_rsa.pub | pulumi config set Modern-Container-Application-Reference-Architecture:aws:SSH_PUBLIC_KEY
cat ~/.ssh/id_rsa | pulumi config set --secret Modern-Container-Application-Reference-Architecture:aws:SSH_PRIATE_KEY
```
