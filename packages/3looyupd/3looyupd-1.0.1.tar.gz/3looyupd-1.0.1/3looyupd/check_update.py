import version as latest_vers

current_version = "1.0.1"
def check_update():
    if latest_vers.latest_version() != current_version:
        print("You are using old version. Please Update")
    else:
        pass