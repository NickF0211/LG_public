
import subprocess
import os

def run_exp(command_header):
    if not os.path.exists('results'):
        os.makedirs('results')


    timeout = 5000
    rule_file  = "player_rule.py"
    FRIEND_THRESHOLDs =  [1, 2, 3, 3, 5]
    Group_Sizes = [2, 3, 4, 5, 6]
    Turn_Around_Playerss = [1, 2, 2, 3, 4]

    for FT, GS, TP in zip(FRIEND_THRESHOLDs, Group_Sizes, Turn_Around_Playerss):

        result_file = "results/{}_{}_{}_opt.txt".format(str(FT), str(GS), str(TP))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [ rule_file, str(FT), str(GS), str(TP)], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/{}_{}_{}_opt_restart.txt".format(str(FT), str(GS), str(TP))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(FT), str(GS), str(TP), "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/{}_{}_{}_opt_bcr.txt".format(str(FT), str(GS), str(TP))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(FT), str(GS), str(TP), "f", "t"], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/{}_{}_{}_opt_ub.txt".format(str(FT), str(GS), str(TP))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(FT), str(GS), str(TP), "f", "f", "t"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        timeout=timeout)
                f.write(result.stdout)
                f.write(result.stderr)

            except subprocess.TimeoutExpired as t:
                f.write("timeout {}".format(timeout))
                #continue



        result_file = "results/{}_{}_{}_opt_all.txt".format(str(FT), str(GS), str(TP))
        print(result_file)
        with open(result_file, 'w') as f:
            try:
                result = subprocess.run(command_header + [rule_file, str(FT), str(GS), str(TP), "t", "t", "t"],
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
    command_header = ["/u/lmarsso/memtime/memtime", "python3"]
    run_exp(command_header)

