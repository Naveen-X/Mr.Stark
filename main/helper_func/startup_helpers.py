import asyncio
import glob
import importlib
import logging
from main_startup import Config
import ntpath
import shlex
from typing import Tuple
import sys
from datetime import datetime
from os import environ, execle, path, remove
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
  

async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
