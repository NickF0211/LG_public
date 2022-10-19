import bank_exp_day
import bank_exp_hour
def run_exp(command_header):
    bank_exp_day.run_exp(command_header)
    bank_exp_hour.run_exp(command_header)

if __name__ == "__main__":
    command_header = ["memtime", "python3"]
    run_exp(command_header)