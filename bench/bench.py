import os
import subprocess


def run_script(vm_path, script_path):
    subprocess.call([vm_path, script_path])

if __name__ == '__main__':
    import timeit
    bench_path = os.path.dirname(os.path.abspath(__file__))

    vms = ['luajit', 'lua', os.path.join(bench_path, '../bin/pylua')]
    bench_scripts = ['bench_loop.l']

    for script in bench_scripts:
        script_path = os.path.join(bench_path, script)
        results = {}
        for vm in vms:
            time = timeit.timeit('run_script("{0}", "{1}")'.format(vm, script_path), setup="from __main__ import run_script", number=10)

            print("Ran script %s with %st, took %lf" % (script, vm, time))
            results[vm] = time
