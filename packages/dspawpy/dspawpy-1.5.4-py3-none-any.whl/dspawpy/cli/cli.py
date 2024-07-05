print("... loading dspawpy cli ...")


def get_args():
    """Get command line arguments"""
    from argparse import ArgumentParser

    ap = ArgumentParser("dspawpy命令行交互小工具/cli")
    ap.add_argument("--hide", default=False, help="隐藏图标/hide logo")
    ap.add_argument("-c", "--check", default=False, help="检查新版本/check new version")
    ap.add_argument("-m", "--menu", default=None, help="选择菜单/select menu")
    ap.add_argument(
        "-l",
        "--language",
        default="CN",
        help="语言/language",
        choices=["CN", "EN"],
    )
    args = ap.parse_args()

    return args


def main():
    """Cli requires main function to run."""
    from loguru import logger

    from dspawpy.cli import aux
    from dspawpy.cli.menu_prompts import Dresponse, Dupdate, logo, menus

    args = get_args()
    lan = args.language

    if not args.hide:
        logger.info(logo[lan])

    aux.verify_dspawpy_version(args.check, lan)

    while True:
        if args.menu:
            menu = args.menu
        else:
            all_supported_tasks = [str(i + 1) for i in range(13)]  # 1-13
            all_supported_subtasks = [
                "31",
                "32",
                "33",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "61",
                "62",
                "81",
                "82",
                "83",
                "84",
                "85",
                "86",
                "87",
                "91",
                "92",
                "93",
                "101",
                "102",
                "103",
                "104",
                "105",
                "131",
                "132",
            ]  # for program
            menu = aux.get_input(
                menus[lan][0],
                all_supported_tasks + all_supported_subtasks + ["q"],
            )

        if menu == "1":
            D = {}
            cmd = "pip install -U dspawpy"
            yn = aux.get_input(
                f"{Dupdate[lan][0]}\n {cmd}\n (y/n)? ",
                ["y", "n"],
                allow_empty=True,
                default_user_input="n",
            )
            D["menu"] = 1
            D["yn"] = yn
            if yn.lower() == "y":
                from os import system

                if system(cmd) == 0:
                    result = [f">>>>>> {Dupdate[lan][1]}", f"{Dupdate[lan][2]}"]
                else:
                    result = [f"!!!!!! {Dupdate[lan][3]}"]
                logger.info("\n".join(result))

        elif menu == "2":
            aux.s2(lan)

        elif menu == "3":
            valid_selection = [str(i) for i in range(4)]
            submenu = aux.get_input(menus[lan][3], valid_selection)
            if submenu == "1":
                aux.s3_1(lan)
            elif submenu == "2":
                aux.s3_2(lan)
            elif submenu == "3":
                aux.s3_3(lan)
            else:
                continue
        elif menu == "31":
            aux.s3_1(lan)
        elif menu == "32":
            aux.s3_2(lan)
        elif menu == "33":
            aux.s3_3(lan)

        elif menu == "4":
            valid_selection = [str(i) for i in range(7)]
            submenu = aux.get_input(menus[lan][4], valid_selection)
            if submenu == "1":
                aux.s4_1(lan)
            elif submenu == "2":
                aux.s4_2(lan)
            elif submenu == "3":
                aux.s4_3(lan)
            elif submenu == "4":
                aux.s4_4(lan)
            elif submenu == "5":
                aux.s4_5(lan)
            elif submenu == "6":
                aux.s4_6(lan)
            else:
                continue
        elif menu == "41":
            aux.s4_1(lan)
        elif menu == "42":
            aux.s4_2(lan)
        elif menu == "43":
            aux.s4_3(lan)
        elif menu == "44":
            aux.s4_4(lan)
        elif menu == "45":
            aux.s4_5(lan)
        elif menu == "46":
            aux.s4_6(lan)

        elif menu == "5":
            valid_selection = [str(i) for i in range(7)]
            submenu = aux.get_input(menus[lan][5], valid_selection)
            if submenu == "1":
                aux.s5_1(lan)
            elif submenu == "2":
                aux.s5_2(lan)
            elif submenu == "3":
                aux.s5_3(lan)
            elif submenu == "4":
                aux.s5_4(lan)
            elif submenu == "5":
                aux.s5_5(lan)
            elif submenu == "6":
                aux.s5_6(lan)
            else:
                continue
        elif menu == "51":
            aux.s5_1(lan)
        elif menu == "52":
            aux.s5_2(lan)
        elif menu == "53":
            aux.s5_3(lan)
        elif menu == "54":
            aux.s5_4(lan)
        elif menu == "55":
            aux.s5_5(lan)
        elif menu == "56":
            aux.s5_6(lan)

        elif menu == "6":
            valid_selection = [str(i) for i in range(3)]
            submenu = aux.get_input(menus[lan][6], valid_selection)
            if submenu == "1":
                aux.s6_1(lan)
            elif submenu == "2":
                aux.s6_2(lan)
            else:
                continue
        elif menu == "61":
            aux.s6_1(lan)
        elif menu == "62":
            aux.s6_2(lan)

        elif menu == "7":
            aux.s7(lan)

        elif menu == "8":
            valid_selection = [str(i) for i in range(8)]
            submenu = aux.get_input(menus[lan][8], valid_selection)
            if submenu == "1":
                aux.s8_1(lan)
            elif submenu == "2":
                aux.s8_2(lan)
            elif submenu == "3":
                aux.s8_3(lan)
            elif submenu == "4":
                aux.s8_4(lan)
            elif submenu == "5":
                aux.s8_5(lan)
            elif submenu == "6":
                aux.s8_6(lan)
            elif submenu == "7":
                aux.s8_7(lan)
            else:
                continue
        elif menu == "81":
            aux.s8_1(lan)
        elif menu == "82":
            aux.s8_2(lan)
        elif menu == "83":
            aux.s8_3(lan)
        elif menu == "84":
            aux.s8_4(lan)
        elif menu == "85":
            aux.s8_5(lan)
        elif menu == "86":
            aux.s8_6(lan)
        elif menu == "87":
            aux.s8_7(lan)

        elif menu == "9":
            valid_selection = [str(i) for i in range(4)]
            submenu = aux.get_input(menus[lan][9], valid_selection)
            if submenu == "1":
                aux.s9_1(lan)
            elif submenu == "2":
                aux.s9_2(lan)
            elif submenu == "3":
                aux.s9_3(lan)
            else:
                continue
        elif menu == "91":
            aux.s9_1(lan)
        elif menu == "92":
            aux.s9_2(lan)
        elif menu == "93":
            aux.s9_3(lan)

        elif menu == "10":
            valid_selection = [str(i) for i in range(6)]
            submenu = aux.get_input(menus[lan][10], valid_selection)
            if submenu == "1":
                aux.s10_1(lan)
            elif submenu == "2":
                aux.s10_2(lan)
            elif submenu == "3":
                aux.s10_3(lan)
            elif submenu == "4":
                aux.s10_4(lan)
            elif submenu == "5":
                aux.s10_5(lan)
            else:
                continue
        elif menu == "101":
            aux.s10_1(lan)
        elif menu == "102":
            aux.s10_2(lan)
        elif menu == "103":
            aux.s10_3(lan)
        elif menu == "104":
            aux.s10_4(lan)
        elif menu == "105":
            aux.s10_5(lan)

        elif menu == "11":
            aux.s11(lan)

        elif menu == "12":
            aux.s12(lan)

        elif menu == "13":
            valid_selection = [str(i) for i in range(3)]
            submenu = aux.get_input(menus[lan][13], valid_selection)
            if submenu == "1":
                aux.s13_1(lan)
            elif submenu == "2":
                aux.s13_2(lan)
            else:
                continue
        elif menu == "131":
            aux.s13_1(lan)
        elif menu == "132":
            aux.s13_2(lan)
        elif menu == "q":
            logger.info(Dresponse[lan][13])
            import sys

            sys.exit()

        icontinue = input(Dresponse[lan][14])
        if icontinue != "y":
            logger.info(Dresponse[lan][13])
            import sys

            sys.exit()


if __name__ == "__main__":
    main()
