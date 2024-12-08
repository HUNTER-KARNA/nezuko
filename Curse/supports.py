from Curse import DEV_USERS, OWNER_ID, SUDO_USERS, WHITELIST_USERS
from Curse.database.support_db import SUPPORTS

async def load_support_users():
    support = SUPPORTS()

    def safe_insert(user_list, user_type):
        for i in user_list:
            try:
                if i:
                    support.insert_support_user(int(i), user_type)
            except ValueError:
                pass

    safe_insert(DEV_USERS, "dev")
    safe_insert(SUDO_USERS, "sudo")
    safe_insert(WHITELIST_USERS, "whitelist")

    return

def get_support_staff(want="all"):
    support = SUPPORTS()
    devs = support.get_particular_support("dev")
    sudo = support.get_particular_support("sudo")
    whitelist = support.get_particular_support("whitelist")

    if want in ["dev", "dev_level"]:
        wanted = devs
    elif want == "sudo":
        wanted = sudo
    elif want == "whitelist":
        wanted = whitelist
    elif want == "sudo_level":
        wanted = sudo + devs
    else:
        wanted = list(set([int(OWNER_ID)] + devs + sudo + whitelist))

    return wanted
