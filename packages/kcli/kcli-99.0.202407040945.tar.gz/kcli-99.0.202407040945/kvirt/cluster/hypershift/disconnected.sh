#!/usr/bin/env bash
oc -n openshift-config get cm user-ca-bundle -o yaml | grep -vE "uid|resourceVersion|creationTimestamp|namespace" | sed "s/openshift-config/hypershift/g" | oc -n hypershift apply -f -
oc -n hypershift patch deployment/operator -p '{"spec":{"template":{"spec":{"$setElementOrder/containers":[{"name":"operator"}],"$setElementOrder/volumes":[{"name":"user-ca-bundle"},{"name":"serving-cert"}],"containers":[{"$setElementOrder/volumeMounts":[{"mountPath":"/etc/pki/tls/certs/"},{"mountPath":"/var/run/secrets/serving-cert"}],"name":"operator","volumeMounts":[{"mountPath":"/etc/pki/tls/certs/","name":"user-ca-bundle"}]}],"volumes":[{"configMap":{"name":"user-ca-bundle"},"name":"user-ca-bundle"}]}}}}'
oc -n hypershift patch deployment/operator -p '{"spec":{"template":{"spec":{"$setElementOrder/containers":[{"name":"operator"}],"containers":[{"args":["run","--namespace=$(MY_NAMESPACE)","--pod-name=$(MY_NAME)","--metrics-addr=:9000","--enable-ocp-cluster-monitoring=false","--enable-ci-debug-output=false","--private-platform=None","--cert-dir=/var/run/secrets/serving-cert","--enable-uwm-telemetry-remote-write","--registry-overrides=\"quay.io/openshift-release-dev/ocp-v4.0-art-dev@{{ hypershift_tag }}={{ disconnected_url }}/openshift/release@{{ hypershift_tag }},quay.io/openshift-release-dev/ocp-v4.0-art-dev@{{ mco_tag }}={{ disconnected_url }}/openshift/release@{{ mco_tag }}\""],"name":"operator"}]}}}}'
