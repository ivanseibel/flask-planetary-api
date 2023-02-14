#!/bin/sh

# 1. Push to remote named "github"
git push -u github main

# 2. Push to remote named "origin"
git push -u origin HEAD:develop
