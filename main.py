from kubernetes import client, config, watch
import pandas as pd
import numpy as np
import datetime
import re

config.kube_config.load_kube_config(config_file="C:\IT技术研究\pythonProject_kubernetes/kubeconfig.yaml")

# 获取API的Corev1Api版本对象
v1_core = client.CoreV1Api()
v1_apps = client.AppsV1Api()

batch = client.BatchV1Api()

job_name = 'hello'
watcher = watch.Watch()
for event in watcher.stream(
        batch.list_namespaced_job,
        namespace='default',
        label_selector=f'job-name={job_name}'):
    assert isinstance(event, dict),"正常"
    print(isinstance(event, dict))
    job = event['object']
    assert isinstance(job, client.V1Job)
    print(isinstance(job, client.V1Job))

