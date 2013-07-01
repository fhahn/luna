import os
import subprocess


bench_path = os.path.dirname(os.path.abspath(__file__))

def run_script(vm_path, args, script_path):
    if len(args) == 0:
        subprocess.call([vm_path, script_path])
    else:
        subprocess.call([vm_path, args, script_path])

if __name__ == '__main__':
    import timeit

    vms = [
            ('luajit', ""),
            ("luajit", "-joff"), ('lua', ""),
            #("python", os.path.join(bench_path, '../luna/main.py')),
            (os.path.join(bench_path, '../bin/luna'),"")
    ]
    bench_scripts = ['bench_loop.l', 'bench_fib.l', 'bench_mergesort.l']

    for script in bench_scripts:
        print("Running benchmark %s" % script)
        script_path = os.path.join(bench_path, script)
        results = {}
        for vm in vms:
            time = timeit.timeit('run_script("{0}", "{1}", "{2}")'.format(vm[0], vm[1], script_path), setup="from __main__ import run_script", number=5)

            print("\t %s took %lf" % (vm[0], time))
            results[vm] = time

        print("")
        for k, v in results.iteritems():
            if k != vms[-1]:
                # compare vm to luna
                factor = results[vms[-1]] / v
                print("\tVm %s is %lf faster than luna" % (k[0], factor))
