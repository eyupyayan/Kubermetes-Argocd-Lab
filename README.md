# Kubernetes + Argo CD Lab Project

Dette prosjektet er et læringsprosjekt for å forstå:

* Docker og container-bygging
* Kubernetes grunnleggende ressurser (Deployment, Service, ConfigMap, Secret, Ingress)
* GitOps med Argo CD
* YAML-struktur og miljø-overlays (Kustomize)

Prosjektet kjører lokalt med **WSL + Docker Desktop + Kubernetes**.

---

## Mål

Gjennom dette prosjektet lærer du:

* Hvordan bygge et Docker-image selv
* Hvordan deploye en app til Kubernetes
* Hvordan konfigurere miljøvariabler og secrets
* Hvordan bruke probes (health checks)
* Hvordan bruke Argo CD til automatisk deploy fra Git

---

## Teknologi

* Python Flask (demo web-app)
* Docker
* Kubernetes (Docker Desktop cluster)
* Argo CD
* Git
* Kustomize

---

## Prosjektstruktur

```
kubernetes-argocd-lab/
│
├─ app/
│   ├─ app.py
│   ├─ requirements.txt
│   └─ Dockerfile
│
├─ k8s/
│   ├─ base/
│   │   ├─ namespace.yaml
│   │   ├─ deployment.yaml
│   │   ├─ service.yaml
│   │   ├─ configmap.yaml
│   │   ├─ secret.yaml
│   │   └─ ingress.yaml
│   │
│   └─ overlays/
│       └─ dev/
│           ├─ kustomization.yaml
│           └─ patch-replicas.yaml
│
└─ argocd-app.yaml
```

---

## Forutsetninger

* Windows med WSL2
* Docker Desktop installert
* Kubernetes aktivert i Docker Desktop
* Git installert
* `kubectl` tilgjengelig i terminal

Test Kubernetes:

```
kubectl get nodes
```

---

## Steg 1 – Bygg Docker-image

Gå til prosjektroten og kjør:

```
docker build -t <dockerhub-bruker>/kubelab-flask-demo:1.0 ./app
```

Sjekk at imaget finnes:

```
docker images
```

---

## Steg 2 – Push til Docker Hub

Logg inn:

```
docker login
```

Push:

```
docker push <dockerhub-bruker>/kubelab-flask-demo:1.0
```

---

## Steg 3 – Oppdater Deployment

I `deployment.yaml`:

```yaml
image: <dockerhub-bruker>/kubelab-flask-demo:1.0
imagePullPolicy: Always
```

---

## Steg 4 – Deploy til Kubernetes (manuelt først)

```
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secret.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
```

Sjekk status:

```
kubectl -n kubelab get all
```

Port-forward for testing:

```
kubectl -n kubelab port-forward svc/flask-demo 8080:80
```

Åpne nettleser:

```
http://localhost:8080
```

---

## Steg 5 – Kustomize Overlay (Dev miljø)

Deploy med overlay:

```
kubectl apply -k k8s/overlays/dev
```

Dette endrer f.eks. replicas uten å kopiere YAML.

---

## Steg 6 – Installer Argo CD

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Vent til pods kjører:

```
kubectl -n argocd get pods
```

Port-forward UI:

```
kubectl -n argocd port-forward svc/argocd-server 8081:443
```

Åpne:

```
https://localhost:8081
```

Finn admin-passord:

```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

---

## Steg 7 – GitOps med Argo CD

Push prosjektet til GitHub/GitLab.

Opprett `argocd-app.yaml` og apply:

```
kubectl apply -f argocd-app.yaml
```

Argo CD vil nå:

* lese YAML fra Git
* deploye automatisk
* rette “drift” hvis cluster endres manuelt

---

## Læringsoppgaver

**Oppgave 1 – Endre ConfigMap**

* Endre farge/verdi
* Commit + push
* Se pods rullere

**Oppgave 2 – Skaler replicas**

* Endre replicas i overlay
* Push
* Se automatisk oppdatering

**Oppgave 3 – Self-heal**

* Skaler manuelt med kubectl
* Se Argo sette tilbake til Git-verdien

---

## Vanlige Feil

**ImagePullBackOff**

* Feil image-navn
* Ikke pushet image
* Ikke logget inn i Docker Hub

**Pods starter ikke**

* Sjekk logs:

```
kubectl logs <podnavn> -n kubelab
```

---

## Neste Steg

Når dette fungerer kan du utvide med:

* Horizontal Pod Autoscaler (HPA)
* CPU / Memory limits
* Rolling Updates
* RBAC i Argo CD
* Multiple miljøer (prod/dev)

---

## Oppsummering

Du lærer hele flyten:

```
Kode → Docker Image → Registry → Kubernetes → Argo CD → GitOps
```

Dette prosjektet gir en praktisk forståelse av hvordan moderne DevOps-miljøer fungerer i praksis.
