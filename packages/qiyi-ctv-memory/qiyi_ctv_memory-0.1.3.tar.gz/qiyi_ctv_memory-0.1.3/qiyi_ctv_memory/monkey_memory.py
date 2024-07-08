# -*- coding: utf-8 -*--
import argparse
import codecs
import datetime
import json
import os

import javaHeap

import Adb

import snapshot_check
import snapshot_get


def trigger_native_dump(deviceIp, package_name, outputPath, outputFile, memoryLevel):
    print("Triggering native.dump")
    memory_level_int = 0
    if memoryLevel == 'high':
        memory_level_int = 3
    elif memoryLevel == 'medium':
        memory_level_int = 2
    else:
        memory_level_int = 1
    snapshot_path = os.path.join(outputPath, "snapshot")
    snapshot_check_result_path = os.path.join(outputPath, "snapshot_check_result")
    snapshot_get.pullSnapShot("adb -s {} ".format(deviceIp), package_name, snapshot_path)
    over_size_so, result, groups = snapshot_check.check_snapshot(snapshot_path, snapshot_check_result_path, memory_level_int)
    if over_size_so != "":
        json_list = []
        if os.path.exists(outputFile):
            with open(outputFile) as f:
                content = f.read()
                if len(content) > 0:
                    json_list = json.loads(content)
        new_node = {
            u"title": u"native占用异常-{}".format(over_size_so),
            u"level": u"2",
            u"type": u"native",
            u"owner": u"wangjianqiang@qiyi.com",
            u"msg": result
        }
        json_list.append(new_node)
        with codecs.open(outputFile, 'w', encoding='utf-8') as file:
            json.dump(json_list, file, ensure_ascii=False, indent=4)

def trigger_total_memory_dump():
    print("Triggering dump.memory")

def classify_device(total_memory_mb):
    if total_memory_mb > 2048:
        return 'high'
    elif 1024 <= total_memory_mb <= 2048:
        return 'medium'
    else:
        return 'low'

thresholds = {
        'high': {'dalvik': 80, 'native': 150, 'total': 450},
        'medium': {'dalvik': 60, 'native': 120, 'total': 300},
        'low': {'dalvik': 40, 'native': 50, 'total': 200}
}

def check_memory(mappingPath, is_timed, outputPath, deviceIp, total_memory_mb, process_total_mb, dalvik_memory_mb, native_memory_mb):
    # Device classification
    memoryLevel = classify_device(total_memory_mb)
    now = datetime.datetime.now()
    # 格式化当前时间
    formatted_time = now.strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3]
    outputFile = os.path.join(outputPath, "memory_warn_{}.json".format(formatted_time))



    adb = Adb(deviceIp)
    package_name = adb.get_current_package_name()
    if is_timed:
        hprof = javaHeap.dumpHprof(adb, str(formatted_time),outputPath)
        #这里添加dumpnative，后边执行比较慢
        trigger_native_dump(deviceIp, package_name, outputPath, outputFile, memoryLevel)

        json = javaHeap.parseLeak(hprof,outputPath,mappingPath)
        javaHeap.parse_json_and_find_bug(json,outputFile,False)
    else:
        # Get thresholds for the current device class
        current_thresholds = thresholds[memoryLevel]

        # Check dalvik memory
        if dalvik_memory_mb > current_thresholds['dalvik']:
            hprof = javaHeap.dumpHprof(adb, str(formatted_time),outputPath)
            json = javaHeap.parseAll(hprof,outputPath,mappingPath)
            javaHeap.parse_json_and_find_bug(json,outputFile,True)
        # Check native memory
        elif native_memory_mb > current_thresholds['native']:
            trigger_native_dump(deviceIp, package_name, outputPath, outputFile, memoryLevel)
        # Check total process memory
        elif process_total_mb > current_thresholds['total']:
            trigger_total_memory_dump()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Memory monitoring script for monkey testing.")
    parser.add_argument('-t', '--timed', action='store_true', help="Whether it is a timed trigger")
    parser.add_argument('-m', '--total_memory', type=int, required=True, help="Total device memory in MB")
    parser.add_argument('-p', '--process_memory', type=int, required=True, help="Total process memory in MB")
    parser.add_argument('-d', '--dalvik_memory', type=int, required=True, help="Dalvik process memory in MB")
    parser.add_argument('-n', '--native_memory', type=int, required=True, help="Native process memory in MB")

    args = parser.parse_args()

    # check_memory_triggers(args.timed, args.total_memory, args.process_memory, args.dalvik_memory, args.native_memory)