# P2-W1 — Oracle Cloud, Ubuntu & K3s Setup

## Goal

Set up a free Oracle Cloud ARM64 VM for the Weather Intelligence Platform and prepare it for Kubernetes/K3s.

## 1. Oracle Cloud & VM

- Created Oracle Cloud Free Tier account.
- Region: **UK South (London)**
- VM: `weather-platform-k3s`
- OS: **Ubuntu 24.04.4 LTS Minimal**
- Architecture: **ARM64 / aarch64**
- Shape: **VM.Standard.A1.Flex**
- CPU: **1 OCPU**
- RAM: **6 GB**
- Disk: **~45 GB**
- Public IP: `145.241.229.125`
- Private IP: `10.0.0.245`

**Why:** A1 is Oracle's Always Free ARM option. Ubuntu Minimal is lightweight and suitable for a server/K3s environment.

### Problem: A1 capacity

Initially, Oracle showed the A1 shape as unavailable in London across AD1, AD2 and AD3.

**Resolution:** Continued checking the available configuration until an A1 instance could successfully be created. The final Ubuntu VM was created successfully.

## 2. SSH into Ubuntu

Private key:

```text
~/Downloads/ssh-key-2026-08-19.key
```

Secure the key:

```bash
chmod 400 ~/Downloads/ssh-key-2026-08-19.key
```

Connect:

```bash
ssh -i ~/Downloads/ssh-key-2026-08-19.key ubuntu@145.241.229.125
```

**Why:** SSH allows secure remote access to the Oracle VM.

First connection asked whether the server was trusted. Entered:

```text
yes
```

## 3. Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

**Why:** Updated the package information and installed available system updates.

## 4. Added 2 GB Swap

Checked memory:

```bash
free -h
```

Created and enabled swap:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Made it permanent:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Checked:

```bash
swapon --show
```

Result:

```text
/swapfile file 2G 0B -2
```

**Why:** The VM only has 6 GB RAM. Swap provides a safety buffer if memory becomes temporarily limited.

## 5. Checked the VM

```bash
nproc
```

Result: `1` CPU

```bash
df -h /
```

Result: `45G total / 41G available`

```bash
uname -m
```

Result:

```text
aarch64
```

**Why:** Confirmed CPU, disk space and ARM64 architecture before installing Kubernetes.

## 6. Checked networking

```bash
ip addr
```

Result:

```text
enp0s6
10.0.0.245/24
UP
```

Checked DNS:

```bash
systemctl is-active systemd-resolved
```

Result:

```text
active
```

**Why:** Confirmed that networking and DNS were working before installing K3s.

# 7. Installed K3s

Installed K3s with:

```bash
curl -sfL https://get.k3s.io | sh -
```

K3s installed:

```text
v1.36.3+k3s1
```

**Why:** K3s is a lightweight Kubernetes distribution, making it suitable for our small Oracle VM.

## 8. Verified K3s

Checked the K3s service:

```bash
sudo systemctl status k3s --no-pager
```

Result:

```text
Active: active (running)
```

Checked the Kubernetes node:

```bash
sudo k3s kubectl get nodes
```

Result:

```text
weather-platform-k3s   Ready   control-plane
```

Checked Kubernetes pods:

```bash
sudo k3s kubectl get pods -A
```

Important system components were running:

```text
CoreDNS
Metrics Server
Traefik
Local Path Provisioner
```

**Why:** Confirmed that K3s and the Kubernetes control plane were working correctly.

## 9. Configured normal kubectl

Initially:

```bash
kubectl get nodes
```

failed with:

```text
permission denied
/etc/rancher/k3s/k3s.yaml
```

### Problem

The K3s kubeconfig belonged to `root`, so the normal `ubuntu` user could not read it.

### Resolution

Created a user kubeconfig:

```bash
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown ubuntu:ubuntu ~/.kube/config
chmod 600 ~/.kube/config
```

Tested it directly:

```bash
kubectl --kubeconfig ~/.kube/config get nodes
```

Result:

```text
weather-platform-k3s   Ready   control-plane
```

Then configured it permanently:

```bash
echo 'export KUBECONFIG=$HOME/.kube/config' >> ~/.bashrc
source ~/.bashrc
```

Now:

```bash
kubectl get nodes
```

works normally.

Also verified:

```bash
kubectl get pods -A
```

and the Kubernetes system pods were running.

# Current Status

```text
Oracle Cloud account       ✅
A1 ARM64 VM                ✅
Ubuntu 24.04               ✅
SSH access                 ✅
System updated             ✅
2 GB swap                  ✅
Networking                 ✅
DNS                        ✅
K3s installed              ✅
Kubernetes node Ready      ✅
kubectl configured         ✅
```

## Current architecture

```text
Oracle Cloud
     ↓
Ubuntu 24.04 ARM64
     ↓
K3s v1.36.3
     ↓
Single-node Kubernetes
     ├── CoreDNS
     ├── Metrics Server
     ├── Traefik
     └── Local Path Provisioner
```

## Next Step

Review the existing **`k8/` project structure and Kubernetes YAML files** before deploying the Weather Intelligence Platform.

**Important:** Do not run `kubectl apply -f k8/` yet. We first need to check the existing manifests and adapt them for the **1 OCPU / 6 GB ARM64** Oracle VM.
