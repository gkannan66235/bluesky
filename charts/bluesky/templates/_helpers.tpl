{{- define "bluesky.labels" -}}
app.kubernetes.io/name: bluesky
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "bluesky.provenance" -}}
aispace.io/source-repo: {{ .Values.provenance.repo | quote }}
aispace.io/source-branch: {{ .Values.provenance.branch | quote }}
aispace.io/source-path: {{ .Values.provenance.path | quote }}
{{- end }}
