#!/usr/bin/env python3

import subprocess
import sys
import argparse
import io
from typing import TypedDict
import os
import yaml

preprocessor_args = {"OS_NAME": "UNKNOWN"}


class Files(TypedDict):
    files: dict[str, str]


class Preprocessor:
    def __init__(self, src: io.TextIOWrapper, dst: io.TextIOWrapper):
        self.dst = dst
        self.lines = src.readlines()
        self.pos = 0

    def peekline(self):
        if self.pos >= len(self.lines):
            return None
        return self.lines[self.pos]

    def nextline(self):
        if self.pos >= len(self.lines):
            return None
        self.pos += 1
        return self.lines[self.pos - 1]

    def get_directive(self, line: str):
        return line[3:].split(" ")[0]

    def get_directive_args(self, line: str, directive: str):
        return line[4 + len(directive) :]

    def is_directive(self, line: str):
        return line.startswith("# @")

    def check_conditional(self, cond: str):
        # for key, value in PREPROCESSOR_ARGS.items():
        #     cond = cond.replace(key, f'"{value}"')

        return eval(cond, preprocessor_args)

    def handle_directive(self, line):
        directive = self.get_directive(line)
        directive_args = self.get_directive_args(line, directive)

        if directive == "include":
            path = directive_args.replace("~", os.getenv("HOME"))

            path = line[12:-2]
            with open(path, "r") as inc:
                self.dst.writelines(inc.readlines())
        elif directive == "if":
            if not self.check_conditional(directive_args):
                num_if = 0
                line = self.nextline()
                while line is not None:
                    if not self.is_directive(line):
                        line = self.nextline()
                        continue
                    directive = self.get_directive(line)
                    if directive == "if" and num_if == 0:
                        break
                    if directive == "if":
                        num_if += 1
                    elif directive == "endif":
                        num_if -= 1
                    line = self.nextline()

    def run(self):
        line = self.nextline()
        while line is not None:
            if self.is_directive(line):
                self.handle_directive(line)
            else:
                self.dst.write(line)

            line = self.nextline()


def docker_exec(image: str, args: list[str], root: bool = False):
    if root:
        return subprocess.check_output(["docker", "exec", "-u", "0", image] + args)
    else:
        return subprocess.check_output(["docker", "exec", image] + args)


def setup_docker(config):
    # image_name: str = config.docker
    # oskind = docker_exec(image_name, ["uname"]).strip().decode("utf-8")
    # if oskind == "Linux":
    preprocessor_args["OS_NAME"] = "linux"


def setup_local(config):
    if config.os is not None:
        preprocessor_args["OS_NAME"] = config.os
    else:
        preprocessor_args["OS_NAME"] = "macos"


def setup(config):
    if config.docker is not None:
        setup_docker(config)
    else:
        setup_local(config)


def main():
    parser = argparse.ArgumentParser(prog="setup.py")
    parser.add_argument("--docker")
    parser.add_argument("--os", type=str, choices=["linux", "macos"])
    parser.add_argument("--home", type=str)
    config = parser.parse_args(sys.argv[1:])

    setup(config)

    with open("files.yml", "r") as f:
        files: Files = yaml.safe_load(f)

    for source, dest in files["files"].items():
        if config.docker is not None:
            home = "./temp"
        elif config.home is not None:
            home = config.home
        else:
            home = os.getenv("HOME")

        dest = dest.replace("~", home)
        with open(source, "r") as src, open(dest, "w") as dst:
            Preprocessor(src, dst).run()


if __name__ == "__main__":
    main()
