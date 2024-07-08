def latest_vers():
  return "1.0.3"

current_version = "1.0.2"
def check_update():
    if latest_vers() != current_version:
        return "You are using old version. Please Update"
    else:
        pass