
import os
import subprocess

def run_exp(command_header):
    with open("baby_domain_template.txt", 'r') as domain_template:
        domain_content = domain_template.read()

    with open("baby_rule_template.txt", 'r') as rule_template:
        rule_conetent = rule_template.read()

    timeout =5000
    #init value

    if not os.path.exists('results'):
        os.makedirs('results')

    vol_bound = 10000

    outfile = "baby_domain_unbounded.py"
    rule_file = "baby_rule_unbounded.py"
    with open(outfile, 'w') as out_f:
        out_f.write(domain_content.format(pid="None", sid="None", aid="None", time="None"))

    for j in range(1, 8):
        with open(rule_file, 'w') as rule_f:
            rule_f.write(
                rule_conetent.format(domain_file=outfile[:-3], i=j, vol_bound=vol_bound))

        result_file = "results/ph_{}_nonopt.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue


        result_file = "results/ph_{}.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file, "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)

                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/ph_{}_restart.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/ph_{}_bcr.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue

        result_file = "results/ph_{}_all.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "t", "t"], stdout=subprocess.PIPE,
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
