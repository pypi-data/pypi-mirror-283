# -*- coding: utf-8 -*--
import argparse
import json
import operator
import os
import time
import subprocess
import codecs

from memory.Adb import Adb

def dumpHprof(adb, name, output):
    pkg_name = adb.get_current_package_name()
    adb.shelltimeout('am broadcast -a com.gala.video.action.DUMPMEM_JAVA {}'.format(pkg_name))
    pid = adb.get_pid(pkg_name)
    heap_dir = '/sdcard/Android/data/' + pkg_name + '/files/GalaApm/dump/'
    java_heap_file = heap_dir + 'runtime.hprof_' + pid
    dump_complete = checkFileDumpCompleted(adb, java_heap_file)
    if dump_complete:
        output_runtime = name + ".hprof"
        output_runtime = os.path.join(output, output_runtime)
        adb.pull(java_heap_file, output_runtime)
    return output_runtime

def wait_for_file(filepath, timeout=60, poll_interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(filepath):
            # 检查文件是否完全写入（大小稳定）
            initial_size = os.path.getsize(filepath)
            time.sleep(poll_interval)
            if os.path.getsize(filepath) == initial_size:
                return True
        time.sleep(poll_interval)
    return False

def checkFileDumpCompleted(adb, src_file, count=5):
    check_count = 0
    last_params = None
    total_count = 0
    while total_count < 20:
        total_count += 1
        time.sleep(3)
        readlines = adb.shell_output('ls -l {}'.format(src_file))
        if readlines:
            ret = readlines[0]
            if ret is not None:
                if last_params is not None:
                    params = ret.split()
                    if operator.eq(params,last_params):
                        check_count = check_count + 1
                        if check_count >= count:
                            return True
                        continue
                    else:
                        check_count = 0
                        last_params = ret.split()
                        continue
                else:
                    check_count = 0
                    last_params = ret.split()
                    continue
            else:
                check_count += 1
                if check_count > 3:
                    return False
    return True

# def process_json(input_json):
#     data = json.loads(input_json)
#
#     results = {
#         'javaTotal': data.get('javaTotal', 0),
#         'nativeTotal': data.get('nativeTotal', 0)
#     }
#
#     messages = []
#     leak_bitmap_nodes = []
#
#     for entry in data.get("Classs", []):
#         instance = entry.get("instance", "")
#         size = entry.get("size", 0)
#         size = size / 1024 / 1024
#
#         if instance == "android.graphics.Bitmap" :
#             if size > 30:
#                 messages.append("android.graphics.Bitmap total size is larger than 30MB({}MB)".format(str(size)))
#
#                 sorted_bitmaps = sorted(data.get("largerBitmap", []), key=lambda x: x["size"], reverse=True)
#                 top_bitmaps = sorted_bitmaps[:10]
#                 results["topBitmaps"] = [
#                     {
#                         "instance": b["instance"],
#                         "size": b["size"],
#                         "resolution": b["resolution"]
#                     } for b in top_bitmaps
#                 ]
#
#         elif instance == "java.lang.String" :
#             if size > 10:
#                 messages.append("java.lang.String total size is larger than 10MB({}MB)".format(str(size)))
#
#         elif size > 5:
#             messages.append("{} total size is larger than 5MB({}MB)".format(instance,str(size)))
#
#     for entry in data.get("largerBitmap", []):
#         if entry.get("type") == "LeakBitmap":
#             node = {
#                 'view': entry.get('view', 'N/A'),
#                 'resolution': entry.get('resolution', 'N/A'),
#                 'trace': entry.get('trace', 'N/A'),
#                 'msg': 'Bitmap resolution is {}, trace is {}'.format(
#                     entry.get('resolution', 'N/A'),
#                     entry.get('trace', 'N/A')
#                 ),
#                 'reason': 'Trace: {}'.format(entry.get('trace', 'N/A'))
#             }
#             leak_bitmap_nodes.append(node)
#
#     if messages:
#         results["messages"] = messages
#
#     results["LeakBitmapNodes"] = leak_bitmap_nodes
#
#     json_output_path = "output.json"
#     with open(json_output_path, "w") as json_file:
#         json.dump(results, json_file, indent=4)
#
#     return results

def parse_json_and_find_bug(input_file, output_file, out_size):
    with codecs.open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    new_json_list = []

    if "LeakBitmap" in data:
        for item in data["LeakBitmap"]:
            if item.get("size", 0) > 200 * 1024:
                msg = (
                    u"所属文件：{path}\n"
                    u"bitmap实例：{instance}\n"
                    u"所属view：{views}\n"
                    u"关联的context：{contexts}\n"
                    u"分辨率：{resolution}\n"
                    u"占用内存：{size_kb} KB\n"
                    u"bitmap最短gc路径：{trace}\n"
                ).format(
                    path = os.path.splitext(os.path.basename(input_file))[0],
                    instance=item.get("instance", ""),
                    views=item.get("views", ""),
                    contexts=item.get("contexts", ""),
                    resolution=item.get("resolution", ""),
                    size_kb=item.get("size", 0) / 1024,
                    trace=item.get("trace", "").replace(u"<br/>", u"\n")
                )
                new_node = {
                    u"title": u"图片未释放--" + item.get("instance", ""),
                    u"level": u"P2",
                    u"type": u"java",
                    u"owner": item.get("contexts", ""),
                    u"msg": msg
                }
                new_json_list.append(new_node)
    if "LeakActivity" in data:
        for item in data["LeakActivity"]:
            msg = (
                u"泄露的activity：{instances}\n"
                u"trace：{trace}\n"
            ).format(
                instances=item.get("instances", "").replace(u",", u"\n"),
                trace=item.get("trace", "")
            )

            new_node = {
                u"title": u"activity泄露--" + item.get("instances", ""),
                u"level": u"1",
                u"type": u"java",
                u"owner": item.get("instances", ""),
                u"msg": msg
            }
            new_json_list.append(new_node)

    if out_size:
        msg = (
            u"javaTotal：{javaTotal}\n"
            u"nativeTotal：{nativeTotal}\n"
        ).format(
            javaTotal=data.get('javaTotal', 0),
            nativeTotal=data.get('nativeTotal', 0)
        )
        if "Classs" in data:
            for entry in data.get("Classs", []):
                instance = entry.get("instance", "")
                size = entry.get("size", 0) / 1024 / 1024

                if instance == "android.graphics.Bitmap" :
                    if size > 30 :
                        sorted_bitmaps = sorted(data.get("largerBitmap", []), key=lambda x: x["size"], reverse=True)
                        top_bitmaps = sorted_bitmaps[:5]

                        top_bitmap_str = u"\n".join([
                            u"instance: {instance}, size: {size} KB, resolution: {resolution}".format(
                                instance=b["instance"].decode('utf-8'),
                                size=b["size"] / 1024.0,
                                resolution=b["resolution"].decode('utf-8')
                            ) for b in top_bitmaps
                        ])

                    msg += u"\nandroid.graphics.Bitmap total size is larger than 30MB({}MB)\n".format(str(size)) + top_bitmap_str

                elif instance == "java.lang.String" and size > 10:
                    msg += u"java.lang.String total size is larger than 10MB({}MB)\n".format(str(size))

                elif size > 5:
                    msg += u"{} total size is larger than 5MB({}MB)".format(instance,str(size))
        new_node = {
            u"title": u"java heap 过大",
            u"level": u"2",
            u"type": u"java",
            u"owner": u"maoyongpeng@qiyi.com",
            u"msg": msg
        }
        new_json_list.append(new_node)

    with codecs.open(output_file, 'w', encoding='utf-8') as file:
        json.dump(new_json_list, file, ensure_ascii=False, indent=4)

def parseLeak(hprof, outputPath, mapping):
    if wait_for_file(hprof):
        pass
    else:
        print("Failed to pull file {} within the timeout period.".format(hprof))
    cmd = ["java", "-jar", "heap_analyzer.jar", "-i", hprof, "-o", outputPath, "-m", mapping, "-l", "bitmap,activity"]
    print("Executing Java command: " + " ".join(cmd))
    subprocess.check_call(cmd)
    return hprof.replace('.hprof', '.json')

def parseAll(hprof, outputPath, mapping):
    if wait_for_file(hprof):
        pass
    else:
        print("Failed to pull file {} within the timeout period.".format(hprof))
    cmd = ["java", "-jar", "heap_analyzer.jar", "-i", hprof, "-o", outputPath, "-m", mapping, "-l", "activity",
           "-d","10", "-b","20"]
    print("Executing Java command: " + " ".join(cmd))
    subprocess.check_call(cmd)
    return hprof.replace('.hprof', '.json')

def parse(hprof, outputPath, mapping, arguments):
    java_command = ["java", "-jar", "heap_analyzer", "-i", hprof, "-o", outputPath, "-m", mapping] + arguments
    process = subprocess.Popen(
        java_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    json_name = hprof.replace('.hprof', '.json')
    abs_file_path = os.path.join(outputPath, json_name)
    detail_info = None
    if os.path.exists(abs_file_path):
        with open(abs_file_path, mode='r') as reader:
            detail_info = reader.read()

    # try:
    #     # parse_results = process_json(detail_info) if detail_info else None
    # except Exception as e:
    #     print(e)

def parse_arguments():
    parser = argparse.ArgumentParser(description='argument')
    parser.add_argument('-m', '--mapping', dest='MAPPING',  default='', help='apk mapping')
    parser.add_argument('-o', '--output',  dest='OUTPUT', default='', help='output path')
    parser.add_argument('-n', '--name', dest='NAME', default='', help='test name')
    parser.add_argument('-d', '--device',  dest='DEVICE', default='', help='device ip')
    # remove dest='ACTION', since it is not being used in this script

    args, unknown_args = parser.parse_known_args()
    return args, unknown_args

if __name__ == "__main__":
    args, jar_args = parse_arguments()
    device = args.DEVICE
    name = args.NAME
    outputPath = args.OUTPUT
    mapping = args.MAPPING

    adb = Adb(device)
    hprof = dumpHprof(adb, name, outputPath)
    if hprof:
        parse(hprof, outputPath, mapping, jar_args)