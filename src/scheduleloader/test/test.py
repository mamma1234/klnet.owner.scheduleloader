from scheduleloader.pack_a import module_a
from scheduleloader.pack_b import module_b

def test():
    module_a.mod_echo_a()
    module_b.mod_echo_b()

if __name__ == '__main__':
    test()