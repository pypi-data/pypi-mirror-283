# -*- coding: utf-8 -*--
import argparse
import datetime
import os

import javaHeap

import Adb


def trigger_native_dump():
    print("Triggering native.dump")

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
    if is_timed:
        hprof = javaHeap.dumpHprof(adb, str(formatted_time),outputPath)
        #这里添加dumpnative，后边执行比较慢




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
            trigger_native_dump()
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