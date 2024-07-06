
import configparser


cfg = configparser.ConfigParser()
cfg.read_string("[main]\n" + open(".env", "r").read())


cfgvars_ = ['host', 'sudo']
cfgvars = {}
for cv in cfgvars_:
    v = cfg.get("main", cv)
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        v = v[1:-1]
    cfgvars[cv] = v


print("open heart surgeon 1.0")
print(cfgvars)
