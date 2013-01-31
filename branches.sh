#!/bin/bash

declare -a branches=(master doc web api analytics datm)
for branch in ${branches[*]}
do
  git clone -b $branch git@github.com:tekacs/scrobble-exchange $branch
done

git clone -b git@github.com:tekacs/scrobble-exchange.wiki wiki