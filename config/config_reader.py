import os, yaml
def read_config(env=None):
    path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path, "r") as f: cfg = yaml.safe_load(f)
    default_env = cfg.get("default", "test")
    envs = cfg.get("environments", {})
    use_env = env or default_env
    if use_env not in envs: use_env = default_env
    return envs[use_env]
