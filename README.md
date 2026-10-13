# Seshat 5G Telco Cloud — 5G Workloads & Application Delivery

![System Architecture](https://raw.githubusercontent.com/dnjasper/seshat-infra-platform/main/architecture.png)

This repository contains the **5G application and network-function workload layer** of a three-repository cloud-native Telco Cloud lab running on Amazon EKS.

The environment combines **Open5GS, UERANSIM, a dedicated UPF, N6 gateway, vDU simulation, Flux GitOps, Multus secondary networking, Prometheus monitoring, and container delivery through Amazon ECR**.

The goal is to model and troubleshoot a cloud-native 5G environment across both the **control plane and user plane** rather than simply deploy standalone Kubernetes applications.

## Architecture Role

The project is separated into three repositories:

- **Repo1 — Infrastructure & Orchestration:** AWS, VPC, EKS, IAM, OIDC, ECR, Terraform, and infrastructure CI/CD.
- **Repo2 — Platform, Networking & GitOps:** Flux, Multus, N3/N6 secondary networking, IPAM, monitoring, and workload delivery.
- **Repo3 — 5G Workloads (this repository):** Open5GS, UERANSIM, UPF, N6 gateway, vDU, workload configuration, and application CI/CD.

## 5G Architecture

The deployed environment models both 5G control-plane signaling and user-plane traffic.

```text
                         5G CONTROL PLANE

 UERANSIM UE
      |
      v
 UERANSIM gNB
      |
      | N2 / NGAP
      | SCTP 38412
      v
 Open5GS AMF
      |
      v
 Open5GS 5G Core
      |
      v
 Open5GS SMF
      |
      | N4 / PFCP
      | UDP 8805
      v
      UPF


                          5G USER PLANE

 UERANSIM UE
      |
      v
 UERANSIM gNB
      |
      | N3 / GTP-U
      | UDP 2152
      | Multus + IPVLAN
      v
      UPF
      |
      | N6
      | Multus + IPVLAN
      v
 N6 Gateway
      |
      v
 External Network / Internet
```

## UERANSIM

UERANSIM provides the simulated **5G UE and gNB**.

The gNB dynamically receives its Kubernetes pod address and N3 secondary-network address before generating its runtime configuration.

Current radio/core parameters include:

```text
MCC: 999
MNC: 70
TAC: 1

Slice:
  SST: 1
  SD: 0x111111

N2:
  Protocol: NGAP / SCTP
  AMF Port: 38412

N3:
  gTP-U address supplied from the Multus N3 interface
```

The UE configuration uses:

```text
SUPI: imsi-999700000000001
DNN/APN: internet
Session Type: IPv4

Slice:
  SST: 1
  SD: 0x111111
```

The UE searches for the deployed UERANSIM gNB and establishes a session through the Open5GS core.

## Open5GS 5G Core

The Open5GS workload provides the 5G core control-plane functions used by the simulated RAN.

The workload is delivered declaratively through Flux/Helm resources maintained in this repository.

The environment includes the core functions required for UE registration, authentication, session establishment, and user-plane control.

The AMF terminates the gNB's **N2 NGAP/SCTP** connection while the SMF controls the UPF through the **N4 PFCP** interface.

## User Plane Function

The UPF is deployed separately so its network behavior can be configured and troubleshot directly.

Current UPF configuration includes:

```text
N4 / PFCP:
  Interface: eth0
  Port: UDP 8805

N3 / GTP-U:
  Interface: n3
  Port: UDP 2152

UE Session Network:
  10.45.0.0/16

UE Gateway:
  10.45.0.1

DNN:
  internet

Metrics:
  Port 9090
```

The UPF receives its N3 and N6 secondary interfaces through the Multus networks defined in Repo2.

Linux forwarding is used for N6 traffic leaving the UPF toward the N6 gateway.

## N6 Gateway

A dedicated N6 gateway workload provides the next hop between the UPF's N6 network and the external network path.

This creates a user-plane path that can be inspected and troubleshot hop-by-hop:

```text
UE
 ↓
gNB
 ↓
N3 / GTP-U
 ↓
UPF
 ↓
N6
 ↓
N6 Gateway
 ↓
External Network
```

This design allows troubleshooting of routing, neighbor resolution, Linux forwarding, firewall behavior, NAT, return paths, and packet flow independently at each stage.

## Multus Secondary Networking

The workload pods use the secondary networks defined in Repo2.

The primary Kubernetes interface remains available for cluster communication while Multus attaches dedicated telecom interfaces for the user plane.

```text
Kubernetes eth0
    |
    +---- Cluster / management traffic

Multus N3
    |
    +---- gNB <-> UPF GTP-U traffic

Multus N6
    |
    +---- UPF <-> N6 Gateway data traffic
```

This more closely models telecom network separation than running all traffic through the default Kubernetes pod network.

## vDU Workload

The repository also contains a containerized vDU simulation used to exercise Kubernetes application delivery and observability.

The vDU workload includes:

- Container image definition
- Kubernetes Deployment
- Service
- Horizontal Pod Autoscaler
- ServiceAccount
- PodMonitor
- PrometheusRule
- Flux monitoring integration
- Environment-specific Kustomize configuration

The workload can therefore be used to test deployment, scaling, monitoring, alerting, and secondary-network behavior alongside the 5G core environment.

## CI/CD

The repository contains a GitHub Actions application-delivery pipeline:

```text
Source Change
     |
     v
GitHub Actions
     |
     v
AWS OIDC Authentication
     |
     v
Container Build
     |
     v
Amazon ECR
     |
     v
Kubernetes / Flux Delivery
```

AWS access is performed through GitHub Actions OIDC rather than long-lived AWS access keys.

Repo1 can also initiate the Repo3 application workflow through GitHub's workflow dispatch API after infrastructure orchestration.

## GitOps Delivery

Repo2 acts as the cluster platform/GitOps layer and contains Flux delivery definitions that reference the workloads maintained here.

This keeps responsibilities separated:

```text
Repo1
Infrastructure
    |
    v
Repo2
Platform + GitOps
    |
    v
Repo3
5G Workloads
```

Changes to the desired workload state remain version controlled while Flux reconciles the Kubernetes environment.

## Repository Structure

```text
.
├── .github
│   └── workflows
│       └── app-pipeline.yaml
│
├── apps
│   ├── n6-gateway
│   │   ├── deployment.yaml
│   │   └── kustomization.yaml
│   │
│   ├── open5gs-core
│   │   ├── daemonsets.yaml
│   │   ├── helmrelease.yaml
│   │   ├── kustomization.yaml
│   │   ├── ocirepository.yaml
│   │   ├── storageclass-pv.yaml
│   │   └── values.yaml
│   │
│   ├── ueransim
│   │   ├── gnb-configmap.yaml
│   │   ├── gnb-deployment.yaml
│   │   ├── gnb-service.yaml
│   │   ├── ue-configmap.yaml
│   │   ├── ue-deployment.yaml
│   │   └── kustomization.yaml
│   │
│   ├── upf
│   │   ├── configmap.yaml
│   │   ├── kustomization.yaml
│   │   ├── upf-deployment.yaml
│   │   └── upf-pfcp-service.yaml
│   │
│   └── vdu
│       ├── Dockerfile
│       ├── vdu_simulator.py
│       └── environments
│           └── dev
│               ├── deployment.yaml
│               ├── hpa.yaml
│               ├── kustomization.yaml
│               ├── pod-monitor.yaml
│               ├── prometheus-rule.yaml
│               └── service.yaml
│
└── flux-kustomization.yaml
```

## Technology Stack

| Area | Technology |
|---|---|
| 5G Core | Open5GS |
| RAN / UE Simulation | UERANSIM |
| User Plane | Open5GS UPF |
| N2 | NGAP / SCTP |
| N3 | GTP-U |
| N4 | PFCP |
| Secondary Networking | Multus / IPVLAN |
| Container Platform | Kubernetes / Amazon EKS |
| GitOps | Flux |
| CI/CD | GitHub Actions |
| Container Registry | Amazon ECR |
| Monitoring | Prometheus / Grafana |
| Configuration | Kubernetes YAML / Kustomize / Helm |

## Project Context

This project is designed as a hands-on Telco Cloud integration environment.

It combines traditional telecom concepts such as RAN integration, SCTP, GTP-U, PFCP, control/user-plane separation, and packet-level troubleshooting with cloud-native technologies including Kubernetes, AWS, Terraform, GitHub Actions, Flux, Multus, Prometheus, and Grafana.

The environment is used to practice end-to-end troubleshooting across the application, Kubernetes, Linux networking, cloud infrastructure, and 5G protocol layers.
