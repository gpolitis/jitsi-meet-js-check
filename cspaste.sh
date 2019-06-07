#!/bin/sh

pbpaste | xmllint --xpath '//code/div/text()' - | recode html..ascii
