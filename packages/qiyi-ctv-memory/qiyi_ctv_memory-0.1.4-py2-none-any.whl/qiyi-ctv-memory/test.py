# -*- coding: utf-8 -*--
from memory import monkey_memory

if __name__ == "__main__":
    device = "192.168.199.214:5555"
    mapping = "D:\\memory\\6\\GitvVideo-release-one-gala-uuid-tv14.7.0.182040_e3e22673-182040-auto_player.apk.mapping.txt"
    monkey_memory.check_memory(mapping,False,"D:\\memory\\6",device,1000,200,30,50)