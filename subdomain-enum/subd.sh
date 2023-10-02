#!/bin/bash
while getopts ":d:i:o:" opt; do
    case $opt in
        d) domain="$OPTARG"
        ;;
        i) input="$OPTARG"
        ;;
        o) output="$OPTARG"
        ;;
        \?) echo "Invalid option -$OPTARG" >&2
        ;;
    esac
done

subdomains=$(cat "$input")

for subdomain in $subdomains; do
    ip=$(dig +short "$subdomain.$domain" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$')
    if [ -n "$ip" ]; then
        echo "$subdomain.$domain,$ip" >> "$output"
    fi
    sleep 1
done
