import myDefaults
import os
from glob import glob
import subprocess
try:
    import env
except ImportError:
    pass


def main():
    folders = getAllFolders()
    pullAllInArr(folders)


def getAllFolders():
    includeMyDefaults = True
    envFolders = []

    try:
        includeMyDefaults = env.includeMyDefaults
        envFolders = env.folders
    except (NameError, AttributeError):
        pass

    allFolders = envFolders

    if includeMyDefaults:
        allFolders += myDefaults.folders

    return allFolders


def pullAllInArr(folders):
    for folder in folders:
        processedFolder = processFolder(folder)

        if not os.path.isdir(processedFolder):
            print("{} is not a folder".format(processedFolder))
            return
        if not isGitRepo(processedFolder):
            subFolders = glob("{}*/".format(processedFolder))
            pullAllInArr(subFolders)
            return

        pull(processedFolder)


def processFolder(folder):
    folder = os.path.expanduser(folder)
    return folder


def isGitRepo(folder):
    gitFolder = folder + os.path.sep + ".git"
    return os.path.isdir(gitFolder)


def pull(repoPath):
    command = [
        "git",
        "-C",
        repoPath,
        "pull",
        "--recurse-submodules"
    ]
    print("==============={}===============".format(command))
    subprocess.run(command)

main()