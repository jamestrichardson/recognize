{{- define "recognize.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "recognize.fullname" -}}
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

{{- define "recognize.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "recognize.labels" -}}
helm.sh/chart: {{ include "recognize.chart" . }}
{{ include "recognize.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "recognize.selectorLabels" -}}
app.kubernetes.io/name: {{ include "recognize.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "recognize.redisHost" -}}
{{- if .Values.redis.enabled }}
{{- printf "%s-redis-master" (include "recognize.fullname" .) }}
{{- else }}
{{- .Values.externalRedis.host }}
{{- end }}
{{- end }}

{{- define "recognize.redisPort" -}}
{{- if .Values.redis.enabled }}
{{- print "6379" }}
{{- else }}
{{- .Values.externalRedis.port }}
{{- end }}
{{- end }}

{{- define "recognize.redisPassword" -}}
{{- if .Values.redis.enabled }}
{{- .Values.redis.auth.password }}
{{- else }}
{{- .Values.externalRedis.password }}
{{- end }}
{{- end }}

{{- define "recognize.celeryBrokerUrl" -}}
{{- if .Values.celery.brokerUrl }}
{{- .Values.celery.brokerUrl }}
{{- else }}
{{- $password := include "recognize.redisPassword" . }}
{{- $host := include "recognize.redisHost" . }}
{{- $port := include "recognize.redisPort" . }}
{{- if $password }}
{{- printf "redis://:%s@%s:%s/0" $password $host $port }}
{{- else }}
{{- printf "redis://%s:%s/0" $host $port }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Celery result backend URL
*/}}
{{- define "recognize.celeryResultBackend" -}}
{{- $password := include "recognize.redisPassword" . }}
{{- $host := include "recognize.redisHost" . }}
{{- $port := include "recognize.redisPort" . }}
{{- if $password }}
{{- printf "redis://:%s@%s:%s/0" $password $host $port }}
{{- else }}
{{- printf "redis://%s:%s/0" $host $port }}
{{- end }}
{{- end }}
{{/*
Create the name of the service account to use
*/}}
{{- define "recognize.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "recognize.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
