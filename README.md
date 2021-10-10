# GitLab Automated Backup

Script to automatically locally backup (clone) all the repositories on all their respective branches within your account's access in any GitLab server.

The script conveniently skips the backup on occasions where there are failures or the cloning process is taking to much time.

Developed using:

- [GitPython](https://gitpython.readthedocs.io/en/stable/)
- [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/)

## Usage

- Create a virtual environment:
  ```shell
  $ python -m venv .venv
  ```
- Activate the virtual environment:
  ```shell
  $ source .venv/bin/activate
  ```
- Install the required packages:
  ```shell
  $ pip install -r requirements.txt
  ```
- Fill in your GitLab account credentials in the `configuration.json` file.

    > Make sure to create a `Personal Access Token` on GitLab with full access.  

- Run the script:
  ```shell
  $ python main.py
  ```
  > Make sure that the directory `codebase/` exists and is empty.

> Failure occasions are stored in the `failures.json` file which will be created after the script run completion.
