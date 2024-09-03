import re

def check_missing_root_location(config):
    return "root" not in config

def check_merge_slashes(config):
    merge_slashes = config.get("merge_slashes", "")
    return merge_slashes.lower() == "off"

def check_raw_backend_response_reading(config):
    return "proxy_pass" in config and "internal" in config

def check_unsafe_variable_use(config):
    # Simple check for $args usage
    return "$args" in config

def analyze_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = f.read()
        
        issues = []
        
        if check_missing_root_location(config):
            issues.append("Missing root location directive")
        
        if check_merge_slashes(config):
            issues.append("merge_slashes set to off")
        
        if check_raw_backend_response_reading(config):
            issues.append("Raw backend response reading enabled")
        
        if check_unsafe_variable_use(config):
            issues.append("Unsafe variable ($args) usage detected")
        
        return issues
    
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    config_paths = ["path/to/nginx.conf", "path/to/sites-enabled/default"]
    for path in config_paths:
        issues = analyze_config(path)
        if issues:
            print(f"Security issues found in {path}:")
            for issue in issues:
                print(f"- {issue}")

if __name__ == "__main__":
    main()
