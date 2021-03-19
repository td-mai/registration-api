#!/bin/bash


response=$(curl --write-out "%{http_code}\n" -s -d "{\"email\":\"${1}\", \"password\":\"${2}\"}" -H "Content-Type: application/json" -X POST http://172.18.0.5:5000/api/register)

http_code=$(tail -n1 <<< "$response")
content=$(sed '$ d' <<< "$response")

echo $http_code
echo $content

if [ $http_code -ne 200 ]; then
    exit 1
fi

echo "Enter your activation code:"
read code

curl -d "{\"code\": ${code}}" -H "Content-Type: application/json" -H "Authorization: Basic $(echo -n "${1}:${2}" | base64)" -X POST http://172.18.0.5:5000/api/activate