#!/bin/bash

for d in */; do
	pandoc -o "$d${d%?}.pdf" "$d${d%?}.md"
done

