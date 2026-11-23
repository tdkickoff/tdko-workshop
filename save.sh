#!/bin/sh
# Copies the working folders into the workshop repo and saves them to GitHub (tdkickoff/tdko-workshop).
set -e
W=/home/claude/workshop
cp -a /home/claude/db/. $W/db/; cp -a /home/claude/bank/. $W/bank/; cp -a /home/claude/site-build/. $W/site-build/; cp /home/claude/*.html $W/game-src/
find $W -name __pycache__ -prune -exec rm -rf {} +
cd $W && git add -A
git diff --cached --quiet && { echo "nothing new to save"; exit 0; }
git -c user.name=tdkickoff -c user.email=tdkickoff@users.noreply.github.com commit -q -m "Workshop save $(date -u +%Y-%m-%d\ %H:%M)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git -c push.negotiate=true push -q origin main && echo saved
