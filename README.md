# FlySo — Global Aviation Cadet Application Portal

> **Personal Note:** Becoming an airline pilot has always been my dream. However, as a non-European citizen, I frequently found myself ineligible for sponsored cadet programs simply due to nationality requirements. I built **FlySo** to break down these barriers—creating a seamless, merit-based application platform where citizenship is never a prerequisite to pursuing a passion for flight.

---

## 📌 Project Overview

FlySo is a cloud-native, microservices-based web platform designed to handle cadet application workflows, status tracking, and automated admin notifications. 

The application is deployed on **Azure Kubernetes Service (AKS)** using containerized services, automated database persistence, and secure asynchronous worker nodes.

---

## 🏗️ Architecture & Tech Stack

* **Frontend & Web Portal:** Flask (Python), HTML5/CSS3, HTTP-only authentication cookies
* **Database:** PostgreSQL 16 with Persistent Volume Claims (PVC) on Azure Disk
* **Background Worker:** Asynchronous Python Processing Service
* **Serverless Execution:** Secure serverless function endpoints (automated decision/notification emails)
* **Orchestration & Cloud:** Azure Kubernetes Service (AKS), Docker, Azure Load Balancer
* **Cloud-Based Static Asset Storage:**
   Implemented cloud-based Object Storage (Azure Blob Storage) for external static assets—specifically hosting the application logo to decouple media assets from the web container filesystem and ensure fast, scalable asset delivery.
* **Automated Serverless Email Notification Engine:**
* Triggered automatically upon administrative action (application acceptance or rejection).
* Decoupled from the primary application server using a serverless execution layer (`email sender`), preventing email sending delays from blocking the web portal's user interface.

---

> 🔒 **Role-Based Dashboard:** The web application dynamically adapts its UI depending on the logged-in user:
> - **Applicants:** Can submit and track candidate applications.
> - **Admins:** Can inspect, accept, or reject incoming applications.
## 📁 Repository Structure

---

├── email sender (serverless component)/   # Serverless email dispatch service
│   ├── api/                              # Serverless API logic
│   └── requirements.txt                  # Dependencies for email component
├── k8/                                   # Kubernetes manifests
│   ├── portal/                           # Portal K8s definitions
│   │   ├── portal-deployment.yaml
│   │   ├── portal-secret.yaml
│   │   └── portal-service.yaml
│   ├── postgres/                         # PostgreSQL K8s definitions
│   │   ├── postgres-deployment.yaml
│   │   ├── postgres-pvc.yaml
│   │   ├── postgres-secret.yaml
│   │   └── postgres-service.yaml
│   └── processing/                       # Processing worker K8s definitions
│       ├── processing-deployment.yaml
│       ├── processing-secret.yaml
│       └── processing-service.yaml
├── portal-service/                       # Web portal microservice (Flask)
│   ├── migrations/                       # Database migration scripts
│   ├── src/                              # Portal core application package
│   │   ├── static/                       # CSS, JS, and image assets
│   │   ├── templates/                    # HTML templates
│   │   ├── __init__.py                   # App factory & extension initialization
│   │   ├── models.py                     # Database models
│   │   └── routes.py                     # Application endpoint routes
│   ├── Dockerfile                        # Portal container build instructions
│   ├── requirements.txt                  # Python dependencies for portal
│   └── run.py                            # Application entry point
├── processing-service/                   # Background processing worker
│   ├── Dockerfile                        # Worker container build instructions
│   ├── main.py                           # Worker entry point & execution logic
│   └── requirements.txt                  # Python dependencies for worker
├── .gitignore                            # Untracked Git exclusions
└── README.md                             # Project documentation
