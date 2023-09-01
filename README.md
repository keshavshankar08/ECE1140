# ECE1140
Shared repository for ECE1140 team TIMMOS THE TANK ENGINE
Test - Alex

## Using Git
1. Clone this repository to your local machine
    - Navigate to the `Code`  in the respository
    - Click the green `<>Code` drop down button
    - Click `HTTPS` tab, then copy the link
    - On your local machine, make a folder in your documents named `Trains`
    - Open `Visual Studio Code`
    - In the top menu bar, navigate to `File > Open Folder`, then select the folder named `Trains` you just created
    - Now in the top menu bar, navigate to `Terminal > New Terminal`
    - In this terminal, type `git clone https://github.com/keshavshankar08/ECE1140.git`
    - Now, in the top menu bar, navigate back to `File > Open Folder`, then open the new folder that was cloned inside of `Trains`
2. Make a branch of the repository
    - Now that you have the respository, say you want to make changes to it, you will need to create a branch to make edits on
    - In the terminal, type `git checkout -b type/issue#-description` where type is a task, feature, etc.; issue# is the issue from jira; description is brief words describing the issue
    - Example: `git checkout -b feature/12-adding-train-class-prototype`
3. Add the files to commit
    - Once you have made all necessary changes, you can check the status of edited files using `git status` in the terminal. This command is available at any point to see the progress of your edits.
    - Red files mean edited files that have not been committed, and Green files mean files that have been edited and committed
    - To add the files, type `git add --all` in the terminal to add all files that have been edited
    - If you want to add specific files, simply type `git add <filepath>`
    - Remember that the filepath is always start from the base directory, which in this case is `ECE1140`
4. Committing the files
    - Once you have added all the files you want, commit the files
    - Type `git commit -m "description"` in the terminal, where description is a brief blurb of what you did
    - Example: `git commit -m "updated readme"`
5. Pushing the commit to github
    - Finally, you want to push the commit to github
    - Type `git push --set-upstream origin <branch>` in the terminal
    - Example: `git push --set-upstream origin feature/12-adding-train-class-prototype`
6. Creating a pull request
    - Now that you have pushed your local changes to github, you need to create a pull request in order for other members to see your changes and approve them to be merged to the main codebase
    - In GitHub, navigate to `Pull Requests > Create pull request`, then select the branch that you committed
    - In the settings, you can enter information on what you did, which can include pictures and such
    - Once done, hit create, then under `reviewers`, add someone or multiple people to review your changes
    - Once they are done reviewing, the users should approve the pull request
    - After the user who created the pull request has recieved atleast 2 approvals, they can merge the code to main

