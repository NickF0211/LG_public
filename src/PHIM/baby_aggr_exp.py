
import os
import subprocess

def run_exp(command_header):
    with open("baby_domain_template.txt", 'r') as domain_template:
        domain_content = domain_template.read()

    with open("baby_rule_template_aggr.txt", 'r') as rule_template:
        rule_conetent = rule_template.read()

    timeout = 10000
    init_values = (1, 2, 4)
    #init value

    if not os.path.exists('results'):
        os.makedirs('results')

    time = 5000
    sid = 2
    aid = 2
    pid = 5
    vol_bound = 10
    for i in range(3):
        outfile = "baby_domain_{}.py".format(i)
        rule_file = "baby_rule_aggr_{}.py".format(i)
        with open(outfile, 'w') as out_f:
            out_f.write(domain_content.format(pid =pid, sid =sid, aid= aid, time = time))

        for j in range(1,18):
            with open(rule_file, 'w') as rule_f:
                rule_f.write(
                    rule_conetent.format(domain_file=outfile[:-3],i=j, vol_bound = vol_bound))

            result_file = "results/baby_{}_rule_aggr_{}.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header + [ rule_file, "f", "f", "f", "f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)

            result_file = "results/baby_{}_rule_opt_aggr_{}.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header +[rule_file, "t", "f", "f", "f"], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)

            result_file = "results/baby_{}_rule_opt_aggr_{}_restart.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header + [rule_file, "t", "t", "f", "f"], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)

            result_file = "results/baby_{}_rule_opt_aggr_{}_bcr.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header + [rule_file, "t", "f", "t", "f"], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)


            result_file = "results/baby_{}_rule_opt_aggr_{}_ub.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header + [rule_file, "t", "f", "f", "t"], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)

            result_file = "results/baby_{}_rule_opt_aggr_{}_all.txt".format(i, j)
            print(result_file)
            with open(result_file, 'w') as f:
                try:
                    result = subprocess.run(command_header + [rule_file, "t", "t", "t", "t"], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                            timeout=timeout)
                except subprocess.TimeoutExpired as t:
                    f.write("timeout {}".format(timeout))
                    continue

                f.write(result.stdout)
                f.write(result.stderr)

        time = time * 10
        sid = sid * 10
        aid = aid * 10
        pid = pid * 10
        vol_bound = vol_bound * 10

    outfile = "baby_domain_unbounded.py"
    rule_file = "baby_rule_aggr_unbounded.py"
    with open(outfile, 'w') as out_f:
        out_f.write(domain_content.format(pid="None", sid="None", aid="None", time="None"))

    for j in range(1, 18):
        with open(rule_file, 'w') as rule_f:
            rule_f.write(
                rule_conetent.format(domain_file=outfile[:-3], i=j, vol_bound=vol_bound))

        result_file = "results/baby_unbounded_rule_aggr_{}.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/baby_unbounded_rule_opt_aggr_{}.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file, "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/baby_unbounded_rule_opt_aggr_{}_restart.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/baby_unbounded_rule_opt_aggr_{}_bcr.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/baby_unbounded_rule_opt_aggr_{}_ub.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "f", "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                continue

            f.write(result.stdout)
            f.write(result.stderr)

        result_file = "results/baby_unbounded_rule_opt_aggr_{}_all.txt".format(j)
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, "t", "t", "t", "t"], stdout=subprocess.PIPE,
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
