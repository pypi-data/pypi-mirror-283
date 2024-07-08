def latest_vers():
  return "1.0.1"

current_version = "1.0.1"
def check_update():
    if latest_vers() != current_version:
        return "You are using old version. Please Update"
    else:
        pass