import os
import json

import gitlab
from git import Repo

from configuration import CodebaseConfiguration

from exceptions import TimeoutError

from timeout import timeout

TIMEOUT = 10
FAILURES_EXPORT_PATH = 'failures.json'


class CodebaseBackUpHandler:
    def __init__(self, codebase_configuration: CodebaseConfiguration) -> None:
        self.codebase_configuration = codebase_configuration

        self.gitlab_client = gitlab.Gitlab(
            url=codebase_configuration.url,
            private_token=codebase_configuration.private_token)

        self.failures = []

    def run(self) -> None:
        for project in self.projects:
            project_name = project.name
            print(f'Project: {project_name}')

            os.mkdir(f'codebase/{project_name}/')

            project_http_url = project.http_url_to_repo.split('https://')[1]

            try:
                project_branches = [
                    branch.name for branch in project.branches.list()
                ]
                print(f'Branches: {project_branches}')

            except Exception as e:
                reason = str(e)
                print(f'General failure for project `{project_name}`. '
                      f'Reason: {reason}.')
                self.__add_project_failure(project_name=project_name,
                                           reason=reason)
                print('##########################')
                continue

            for branch in project_branches:
                try:
                    self.__clone_project(project_name=project_name,
                                         project_http_url=project_http_url,
                                         branch=branch)
                    print('**************************')

                except TimeoutError as t:
                    reason = str(t)
                    print(f'Failed to clone project `{project_name}` '
                          f'on branch `{branch}`. Reason: {reason}.')
                    self.__add_branch_failure(project_name=project_name,
                                              branch=branch,
                                              reason=reason)
                    print('##########################')
                    continue

            print('---------------------------------------------------------')

        self.__export_failures_dict()

    @timeout(TIMEOUT)
    def __clone_project(self, project_name: str, project_http_url: str,
                        branch: str) -> None:
        print(f'Cloning project `{project_name}` on branch `{branch}` '
              f'from {project_http_url} ...')
        clone_url = self.__generate_cloning_url(
            project_http_url=project_http_url)
        to_path = self.__generate_to_path(project_name=project_name,
                                          branch=branch)
        os.mkdir(to_path)
        Repo.clone_from(url=clone_url, to_path=to_path, branch=branch)
        print(f'Project cloned to `{to_path}`!')

    def __generate_cloning_url(self, project_http_url: str) -> str:
        username = self.codebase_configuration.username
        password = self.codebase_configuration.password
        return f'https://{username}:{password}@{project_http_url}'

    def __generate_to_path(self, project_name: str, branch: str) -> str:
        return f'codebase/{project_name}/{branch}/'

    def __add_project_failure(self, project_name: str, reason: str) -> None:
        self.failures.append({
            'type': 'Project',
            'project_name': project_name,
            'reason': reason
        })

    def __add_branch_failure(self, project_name: str, branch: str,
                             reason: str) -> None:
        self.failures.append({
            'type': 'Branch',
            'project_name': project_name,
            'branch': branch,
            'reason': reason
        })

    def __export_failures_dict(self) -> None:
        with open(FAILURES_EXPORT_PATH, 'w') as f:
            json.dump(self.failures, f)

    @property
    def projects(self) -> list:
        return self.gitlab_client.projects.list()
