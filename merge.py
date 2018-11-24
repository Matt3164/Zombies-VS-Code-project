"""

Merge files into single file to upload to codingames

"""

import os




def separation_line(n:int):

    return "".join(['-']*n)

if __name__ == '__main__':

    current_dir = os.getcwd()

    target_file = "src_merged.py"

    package_name = "pyzombies"

    list_files_to_merged = [
        "utils/logger.py",
        "utils/list.py",
        "utils/math.py",
        "utils/optimization/criteria.py",
        "utils/optimization/min_criteria.py",
        "utils/optimization/max_criteria.py",
        "utils/optimization/criteria_factory.py",
        "utils/optimization/ordered_multi_criteria_optimizer.py",
        "agents/position.py",
        "agents/person.py",
        "agents/distance.py",
        "agents/zombie.py",
        "agents/human.py",
        "agents/action.py",
        "environment/game_state.py",
        "environment/zvh_game_state.py",
        "agents/allan.py",
        "agents/safe_allan.py",
        "agents/a_bit_smarter_allan.py",
        "strategies/strategy.py",
        "strategies/dumb.py",
        "strategies/safe.py",
        "environment/sensor.py",
    ]

    main_file = "main.py"

    with open(os.path.join(current_dir, target_file), "w") as f_target:
        for filename in list_files_to_merged:

            real_path = os.path.join(
                current_dir,
                package_name,
                filename
            )

            print(real_path)

            assert os.path.exists(real_path)

            with open(real_path,"r") as f_src:

                # src_content = f_src.read()

                src_content = str()

                for line in f_src.readlines():

                    first_word = line.split(' ')[0]

                    if not ( first_word in ["import", "from"] ):
                        src_content += line
                    elif "needed" in line:
                        src_content += line

            f_target.write("\n")

            f_target.write("#" + separation_line(100) + "\n")

            f_target.write(
                "# {0} {1} {2} \n".format(separation_line(25), filename, separation_line(25))
            )

            f_target.write(src_content)

        with open(os.path.join(current_dir, main_file), "r") as f_src:

            src_content = f_src.read()

            f_target.write("\n")

            f_target.write("#" + separation_line(100) + "\n")

            f_target.write(
                "# {0} {1} {2} \n".format(separation_line(25), main_file, separation_line(25))
            )

            f_target.write(src_content)









