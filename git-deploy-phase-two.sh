#!/bin/bash

# Print git status
git status

# Add all changes to the staging area
git add .

#user input for commit message
read readMessage

# Commit changes with a custom message
git commit -m "$readMessage"

# Push the changes to the remote repository
git push

# Run npm command to deploy
output=$(sls deploy)

# Display the captured output
echo "sls deploy output:"

searchString="Deploying"
if [[ $output =~ $searchString ]]; then
  npm install -g serverless
else
  echo "Deploying on AWS"
fi

