
import subprocess
import os

def run_exp(command_header):
    if not os.path.exists('results'):
        os.makedirs('results')


    timeout = 1200
    rule_file  = "graph_rules.py"
    properties_remap = [1,2,3,4]
    properties = [2, 3, 7, 8]
    for j, index in zip(properties, properties_remap):
        result_file = "results/dg_{}.txt".format(index)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file, str(j)], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/dg_{}_restart.txt".format(index)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/dg_{}_bcr.txt".format(index)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue


        result_file = "results/dg_{}_all.txt".format(index)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(j), "t", "t", "f"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue




if __name__ == "__main__":
    command_header = ["memtime", "python3"]
    run_exp(command_header)



