

from typing import List, Optional
import toml
import re
import fnmatch

DEFAULT_PROXY_RULES = [
    {
        "repo": "*",
        "allow": True,
        "use_re": False
    },
    {
        "repo": "*/*",
        "allow": True,
        "use_re": False
    }
]

DEFAULT_CACHE_RULES = [
    {
        "repo": "*",
        "allow": True,
        "use_re": False
    },
    {
        "repo": "*/*",
        "allow": True,
        "use_re": False
    }
]

class OlahRule(object):
    def __init__(self) -> None:
        self.repo = ""
        self.type = "*"
        self.allow = False
        self.use_re = False

    @staticmethod
    def from_dict(data) -> "OlahRule":
        out = OlahRule()
        if "repo" in data:
            out.repo = data["repo"]
        if "allow" in data:
            out.allow = data["allow"]
        if "use_re" in data:
            out.use_re = data["use_re"]
        return out
    
    def match(self, repo_name: str) -> bool:
        if self.use_re:
            return self.match_re(repo_name)
        else:
            return self.match_fn(repo_name)
    
    def match_fn(self, repo_name: str) -> bool:
        return fnmatch.fnmatch(repo_name, self.repo)
    
    def match_re(self, repo_name: str) -> bool:
        return re.match(self.repo, repo_name) is not None

class OlahRuleList(object):
    def __init__(self) -> None:
        self.rules: List[OlahRule] = []
    
    @staticmethod
    def from_list(data) -> "OlahRuleList":
        out = OlahRuleList()
        for item in data:
            out.rules.append(OlahRule.from_dict(item))
        return out
    
    def clear(self):
        self.rules.clear()
    
    def allow(self, repo_name: str) -> bool:
        allow = False
        for rule in self.rules:
            if rule.match(repo_name):
                allow = rule.allow
        return allow

class OlahConfig(object):
    def __init__(self, path: Optional[str] = None) -> None:

        # basic
        self.host = "localhost"
        self.port = 8090
        self.ssl_key = None
        self.ssl_cert = None
        self.repos_path = "./repos"
        self.hf_url = "https://huggingface.co"
        self.hf_lfs_url = "https://cdn-lfs.huggingface.co"
        self.mirror_url = f"http://{self.host}:{self.port}"
        self.mirror_lfs_url = f"http://{self.host}:{self.port}"

        # accessibility
        self.offline = False
        self.proxy = OlahRuleList.from_list(DEFAULT_PROXY_RULES)
        self.cache = OlahRuleList.from_list(DEFAULT_CACHE_RULES)

        if path is not None:
            self.read_toml(path)
        
        # refresh urls
        self.mirror_url = f"http://{self.host}:{self.port}"
        self.mirror_lfs_url = f"http://{self.host}:{self.port}"

    
    def empty_str(self, s: str) -> Optional[str]:
        if s == "":
            return None
        else:
            return s

    def read_toml(self, path: str) -> None:
        config = toml.load(path)

        if "basic" in config:
            basic = config["basic"]
            self.host = basic.get("host", self.host)
            self.port = basic.get("port", self.port)
            self.ssl_key = self.empty_str(basic.get("ssl-key", self.ssl_key))
            self.ssl_cert = self.empty_str(basic.get("ssl-cert", self.ssl_cert))
            self.repos_path = basic.get("repos-path", self.repos_path)
            self.hf_url = basic.get("hf-url", self.hf_url)
            self.hf_lfs_url = basic.get("hf-lfs-url", self.hf_lfs_url)
            self.mirror_url = basic.get("mirror-url", self.mirror_url)
            self.mirror_lfs_url = basic.get("mirror-lfs-url", self.mirror_lfs_url)

        if "accessibility" in config:
            accessibility = config["accessibility"]
            self.offline = accessibility.get("offline", self.offline)
            self.proxy = OlahRuleList.from_list(accessibility.get("proxy", self.proxy))
            self.cache = OlahRuleList.from_list(accessibility.get("cache", self.cache))
