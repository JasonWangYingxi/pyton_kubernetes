from kubernetes import client, config
import pandas as pd
import numpy as np
import datetime
import re

config.kube_config.load_kube_config(config_file="C:\IT技术研究\pythonProject_kubernetes/kubeconfig.yaml")

# 获取API的Corev1Api版本对象
v1_core = client.CoreV1Api()
v1_apps = client.AppsV1Api()

# 列出 namespaces
#for ns in v1_core.list_namespace().items:
#    print(ns.metadata.name)

# 列出所有的services
#ret = v1_core.list_service_for_all_namespaces(watch=False)
#for i in ret.items:
#    print(
#        "%s \t%s \t%s \t%s \t%s \n" % (i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))

# 列出所有的pod
#ret = v1_core.list_pod_for_all_namespaces(watch=False)
#for i in ret.items:
#    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# 列出所有deploy
#ret = v1_apps.list_deployment_for_all_namespaces(watch=False)
#for i in ret.items:
#    print("%s\t%s\t%s" % (i.metadata.namespace, i.metadata.name,i.status))

#以下部分用于分析pod日志
def get_pod_logs(pod_name, namespace):
    return v1_core.read_namespaced_pod_log(name=pod_name, namespace=namespace)
#print(v1_core.read_namespaced_pod_log(name='daemon-test-mxbj7', namespace='default'))
print(get_pod_logs('daemon-test-mxbj7', 'default'))
r = get_pod_logs('daemon-test-mxbj7', 'default')
x = r.split("\n")
char = 0
no_char = 0
log_char = []
log_not_char = []
for i in range(0, len(x)):
    #print(x[i], "\n")
    y = x[i].split(" ")
    #判断y[0]是否为日期
    m = re.match('\d{4}\/\d{2}\/\d{2}',y[0])
    if m is not None:
        #将日期类分到一个字符串数组
        #print(m.group())
        log_char.insert(char, x[i].split(": "))
        char = char + 1
    else:
        #将非日期类分到一个非字符串数组
        #print('None')
        log_not_char.insert(no_char, x[i].split(": "))
        no_char = no_char + 1
print(log_char[0])
print(log_not_char[0])

#找出日期时间相同的日志数量并归类统计
count = 1
st = 0
log_char_st = []
log_char_st.insert(st, log_char[0][0])
st = st + 1
log_char_st.insert(st, log_char[0][1])
print(log_char_st)
for i in range(1, len(log_char)):
    log_char_tm1 = log_char[i][0].split(" ")
    log_char_tm2 = log_char[i-1][0].split(" ")
    if (log_char_tm1[0] == log_char_tm2[0]) and (log_char_tm1[1] == log_char_tm2[1]):
        count = count + 1
        print("找到相同时间的条目，数量增加1，当前为", count)
        st = st + 1
        log_char_st.insert(st, log_char[i][1])
    else:
        st = st + 1
        log_char_st.insert(st, log_char[i][0])
        st = st + 1
        log_char_st.insert(st, log_char[i][1])
print("相同日志数量为", count)
print("相同时间的日志为", log_char_st)

