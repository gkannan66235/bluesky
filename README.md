# bluesky

Sample app for the kagent GitOps demo (Infra-Catalyst `apps/kagent`). A tiny Python HTTP service,
packaged as a Helm chart and deployed by Argo CD. Every object carries `aispace.io/source-*`
annotations pointing back at this repo, so the kagent gitops-agent can turn a live fix into a PR.

```
app/server.py          the service (/, /healthz, /alloc?mb=N)
Dockerfile             image -> crazstarter.azurecr.io/bluesky:<tag>
charts/bluesky/        Helm chart (values.yaml is what gets edited by PRs)
argocd/application.yaml  Argo CD Application (namespace bluesky)
```

## Deploy

```bash
az acr login -n crazstarter
docker build --platform linux/arm64 -t crazstarter.azurecr.io/bluesky:0.1.0 . && docker push crazstarter.azurecr.io/bluesky:0.1.0

kubectl apply -f argocd/application.yaml          # GitOps via Argo CD
# or without Argo CD:
helm upgrade --install bluesky charts/bluesky -n bluesky --create-namespace
kubectl port-forward -n bluesky svc/bluesky 8081:80 && curl localhost:8081
```

## Demo scenarios

| Break it | Symptom | Fix the agent should reconcile in `charts/bluesky/values.yaml` |
|---|---|---|
| `helm upgrade ... --set image.tag=9.9.9` | `ImagePullBackOff` | `image.tag: "0.1.0"` |
| `--set resources.limits.memory=16Mi`, or `curl /alloc?mb=200` under the 128Mi limit | `OOMKilled` | raise `resources.limits.memory` |

Flow: the sre-agent diagnoses and patches the live object, then gitops-agent resolves the owning
repo from the annotations and opens a PR changing `values.yaml`; merging it lets Argo CD converge.

> kagent's `gitops-mcp` talks to the GitHub REST API: give it a fine-grained PAT (Contents RW + Pull
> requests RW on this repo only) via the `github-token` Secret (`apps/kagent/scripts/setup-secrets.sh`).
