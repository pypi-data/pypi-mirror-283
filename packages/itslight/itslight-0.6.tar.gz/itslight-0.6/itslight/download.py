import os
import re
from json import JSONDecodeError
from typing import List


def download(repo: str):
    # minimal = False
    if "--minimal" in repo:
        repo = repo.replace("--minimal", "")
        # minimal = True
        print("--minimal flag is not yet supported at the moment")
        exit(-1)

    fields = re.findall(r"^(?:(.+)\/)?(.+?)(?:\[(.+)\])?$", repo, flags=re.MULTILINE)

    if len(fields) < 1:
        print(f"Invalid repo: {repo}")
        exit(1)

    print()
    for field in fields:
        if not field:
            continue

        repo = (field[0] or "itslight-py") + "/" + field[1] + "/" + (field[2] or "main")

        try:
            config = get_config(repo)
        except JSONDecodeError:
            print("panic: json decoder error for " + repo)
            exit(1)

        print(
            "Getting \033[36m%s\033[0m → \033[2mv%s\033[0m\n"
            % (field[1], config["version"])
        )

        print("  Dependencies:")
        for dep in config["dependencies"]:
            print("  \033[33m+ \033[0m%s" % dep)

        print("\n  hold… ", end="")
        p = pip_install(config["dependencies"])

        if p.returncode != 0:
            print("\033[31m× failed.\033[0m")
            if p.stderr:
                print("\n  " + "\n  ".join(p.stderr.read().decode("utf-8").split("\n")))
            else:
                print("\n  (no associated output from pip)\n")

            exit(1)

        print("\033[32m✔\033[0m\n")

        print("  Files:")
        get_files(field, config["name"])

        print()


def get_files(field, name: str):
    import httpx

    client = httpx.Client()
    res = client.get(
        "https://api.github.com/repos/"
        + (field[0] or "itslight-py")
        + "/"
        + field[1]
        + "/contents/"
        + name,
        params={
            "ref": field[2] or "main"  # branch/commit
        },
    )

    os.makedirs("its/" + name, exist_ok=True)
    for file in res.json():
        if file["type"] == "file":
            print("  \033[36m● \033[0m\033[2mits/\033[0m%s" % file["path"])
            fres = client.get(file["download_url"])
            with open("its/" + file["path"], "wb") as f:
                f.write(fres.content)

        elif file["type"] == "dir":
            get_files(field, name + "/" + file["name"])

    # finally, get the readme
    print("  \033[36m! \033[0m\033[2mits/\033[0m%s" % "definitely/README.md")

    fres2 = client.get(
        "https://raw.githubusercontent.com/"
        + (field[0] or "itslight-py")
        + "/"
        + field[1]
        + "/"
        + (field[2] or "main")
        + "/README.md"
    )
    with open("its/definitely/README.md", "wb") as f:
        f.write(fres2.content)


def get_config(repo: str) -> dict:
    import httpx

    client = httpx.Client()

    res = client.get("https://raw.githubusercontent.com/" + repo + "/itslight.json")

    if res.status_code != 200:
        print(res.text)
        print(f"\033[31m× Error fetching repo ({repo}): {res}\033[0m")
        print()
        exit(1)

    return res.json()


def pip_install(pkgs: List[str]):
    import subprocess, sys

    p = subprocess.Popen(
        f"{sys.executable} -m pip install {' '.join(pkgs)} -qq".split(),
        stdout=subprocess.PIPE,
    )
    p.communicate()
    return p
