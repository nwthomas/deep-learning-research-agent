{{/*
Expand the name of the chart.
*/}}
{{- define "deep-learning-research-agent.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "deep-learning-research-agent.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "deep-learning-research-agent.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "deep-learning-research-agent.labels" -}}
helm.sh/chart: {{ include "deep-learning-research-agent.chart" . }}
{{ include "deep-learning-research-agent.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "deep-learning-research-agent.selectorLabels" -}}
app.kubernetes.io/name: {{ include "deep-learning-research-agent.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "deep-learning-research-agent.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "deep-learning-research-agent.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the image name
*/}}
{{- define "deep-learning-research-agent.image" -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion }}
{{- printf "%s:%s" .Values.image.repository $tag }}
{{- end }}

{{/*
Create configmap name
*/}}
{{- define "deep-learning-research-agent.configmapName" -}}
{{- printf "%s-config" (include "deep-learning-research-agent.fullname" .) }}
{{- end }}

{{/*
Create secret name
*/}}
{{- define "deep-learning-research-agent.secretName" -}}
{{- printf "%s-secret" (include "deep-learning-research-agent.fullname" .) }}
{{- end }}
