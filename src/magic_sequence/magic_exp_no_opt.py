
import subprocess
import os

def run_exp(command_header):
    if not os.path.exists('results'):
        os.makedirs('results')


    timeout = 5000
    rule_file  = "magic_rule_no_opt.py"

    for j in range(1, 10):

        result_file = "results/magic_unbound_N_{}.txt".format(str(j * 50))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file, str(j)], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/magic_unbound_N_{}_restart.txt".format(str(j * 50))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/magic_unbound_N_{}_bcr.txt".format(str(j * 50))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/magic_unbound_N_{}_ub.txt".format(str(j * 50))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "f", "f", "t"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/magic_unbound_N_{}_all.txt".format(str(j * 50))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "t", "t", "t"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

if __name__ == "__main__":
    command_header = ["/u/lmarsso/memtime/memtime", "python3"]
    run_exp(command_header)

