#!/usr/bin/env python3
import os
import re
 
def main():
    os.system('git stash')
    os.system('git pull')
    os.system('git stash apply')
    os.system('git status')

if __name__ == "__main__":
    main()
