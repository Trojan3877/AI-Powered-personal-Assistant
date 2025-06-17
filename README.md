# 🤖 AI-Powered Personal Assistant

A modular, containerized AI Assistant built with OpenAI, Kubernetes, Terraform, Ansible, Helm, and CI/CD.  
Designed for intelligent scheduling, semantic Q&A, Snowflake queries, and scalable cloud-native deployment.

---

## 🧠 Core Features

- ✨ GPT-3.5 Turbo via OpenAI API
- 📅 Scheduling & intelligent reminders
- ❓ Snowflake-powered Q&A fallback to OpenAI
- 🐳 Dockerized for reproducible environments
- ☸️ K8s + Helm for modern orchestration
- ☁️ Terraform + Ansible for infrastructure setup
- 🔁 GitHub Actions for continuous delivery
- 🔐 .env secrets with Helm values support
- 📊 Visual flowchart of system design

---

## 📂 Repository Structure


---

## 🛠️ Technologies Used

| Tool           | Purpose                                   |
|----------------|-------------------------------------------|
| `Python`       | Backend ML/logic                          |
| `OpenAI API`   | Language reasoning / fallback NLP         |
| `Snowflake`    | Structured semantic memory layer          |
| `Docker`       | Local + production containerization       |
| `Kubernetes`   | Cluster orchestration                     |
| `Helm`         | Declarative deployment packaging          |
| `Terraform`    | Cloud infrastructure as code              |
| `Ansible`      | VM/server automation                      |
| `CI/CD`        | GitHub Actions for test + deploy          |

---

## 🚀 Deployment

```bash
# Local Dev
make install
make run

# Dockerized
make docker-build
make docker-run

# Kubernetes (manual)
kubectl apply -f k8s/deployment.yaml

# Terraform (infrastructure provisioning)
terraform init
terraform apply

AI Assistant · Python · OpenAI · Snowflake · DevOps · Kubernetes · Helm · Terraform · Ansible · CI/CD · LLM · GitHub Actions · Docker · Cloud Deployment


![Build](https://github.com/Trojan3877/AI-Powered-personal-Assistant/actions/workflows/ci-cd.yml/badge.svg)


![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/github/license/Trojan3877/AI-Powered-personal-Assistant)
![Build](https://img.shields.io/badge/build-passing-success)
![CI/CD](https://img.shields.io/badge/CI--CD-GitHub%20Actions-blue)
![OpenAI](https://img.shields.io/badge/ML%20Algo-GPT--3.5%20Turbo-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-blue)
![Snowflake](https://img.shields.io/badge/Snowflake-supported-lightblue)
