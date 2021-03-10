#!/usr/bin/env python3

"""
This script checks for new GitHub releases and updates YAML template with them.
"""

import argparse
import io
import logging
import os
import re
import sys
from urllib.parse import urlparse

try:
    from github import Github
except ImportError:
    sys.exit("pygithub python module is required for this script.")

try:
    import ruamel.yaml

    yaml = ruamel.yaml.YAML()
except ImportError:
    sys.exit("yuamel.yaml python module is required for this script.")


def getLatestGHReleaseVersion(github_token, exporter_name, url):
    """
    Gets latest GitHub release for specified repository
    """
    github_repo_path = urlparse(url).path.strip("/")
    g = Github(github_token)
    repo = g.get_repo(github_repo_path)
    releases = repo.get_releases()

    for release in releases:
        if not release.prerelease and not release.draft:
            github_latest_release_tag = release.tag_name
            github_latest_release_body = release.body
            github_latest_release_url = release.html_url
            break

    logging.debug(
        "Latest %s release tag: %s" % (exporter_name, github_latest_release_tag)
    )
    github_latest_release_version = re.search(
        r"\d+\.\d+\.\d+", github_latest_release_tag
    )
    if not github_latest_release_version.group():
        logging.error(
            "Could not get release version for %s from latest release tag: %s"
            % (exporter_name, github_latest_release_tag)
        )
        sys.exit(1)
    else:
        logging.info(
            "Latest %s release version: %s"
            % (exporter_name, github_latest_release_version.group())
        )
        return (
            github_latest_release_version.group(),
            github_latest_release_body,
            github_latest_release_url,
        )


def getGHBranches(github_token):
    """
    Gets existing branches to check if PR is already present
    """
    github_repo_path = "lest/prometheus-rpm"
    logging.debug("Getting list of existing GitHub branches")
    g = Github(github_token)
    branches = []
    for branch in g.get_repo(github_repo_path).get_branches():
        branches.append(branch.name)

    return branches


def updateGHTemplate(
    github_token, filename, branch, message, template, release_notes, url
):
    """
    Creates PR with updated version
    """
    github_repo_path = "lest/prometheus-rpm"
    g = Github(github_token)
    repo = g.get_repo(github_repo_path)

    # create new branch:
    sb = repo.get_branch("master")
    logging.debug("Creating new GitHub branch: %s" % branch)
    repo.create_git_ref(ref="refs/heads/" + branch, sha=sb.commit.sha)

    # format PR body:
    pr_body = "%s\nRelease notes:\n```\n%s\n```" % (url, release_notes)

    logging.debug(pr_body)

    # format YAML file:
    formatted_template = io.BytesIO()
    yaml.explicit_start = True
    yaml.indent(offset=2)
    yaml.dump(template, formatted_template)

    # get existing file checksum:
    file = repo.get_contents(filename)

    # update template in new branch:
    logging.debug("Updating %s with new values" % filename)
    repo.update_file(
        filename, message, formatted_template.getvalue(), file.sha, branch=branch
    )

    # create new pull request:
    logging.debug("Creating new pull request")
    pr = repo.create_pull(title=message, body=pr_body, head=branch, base="master")
    logging.info("Pull request #%u created" % pr.number)


if __name__ == "__main__":
    env_github_token = os.environ.get("GH_TOKEN")
    env_template_config = os.environ.get("TEMPLATE_CONFIG_FILE", "./templating.yaml")

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-l",
        "--loglevel",
        default="info",
        type=str.lower,
        choices=["error", "warning", "info", "debug"],
        help="Set log level to {error,warning,info|normal,debug}",
    )
    parser.add_argument(
        "--templates",
        metavar="N",
        type=str,
        nargs="+",
        default="all",
        help="A list of templates to generate",
    )
    parser.add_argument(
        "--template-config",
        metavar="file",
        type=str,
        default=env_template_config,
        help="The configuration file to generate templates with",
    )
    parser.add_argument(
        "--github-token", type=str, default=env_github_token, help="GitHub API token"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Check mode, does not push changes to GitHub",
    )

    args = parser.parse_args()
    templates = args.templates
    template_config = args.template_config
    github_token = args.github_token
    check_mode = args.check

    # logging settings:
    if args.loglevel == "info":
        logging.basicConfig(level=logging.INFO)
    elif args.loglevel == "warning":
        logging.basicConfig(level=logging.WARNING)
    elif args.loglevel == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    # check if github token is specified
    if not github_token:
        if check_mode:
            logging.warning(
                "GH_TOKEN environment variable is not set, you might hit GitHub API rate limits soon"
            )
        else:
            logging.error(
                "GH_TOKEN environment variable is not set and --github-token argument is not specified, quitting"
            )
            sys.exit(1)

    # load existing template yaml file:
    try:
        with open(template_config, "r") as tc:
            config = yaml.load(tc)
    except IOError:
        logging.error("Couldn't open config file: %s" % template_config)
        sys.exit(1)
    else:
        logging.debug("Configuration file loaded successfully: %s" % template_config)

    # work out which templates we are calculating:
    if templates == "all":
        work = config["packages"]
    else:
        work = {}
        for t in templates:
            work[t] = config["packages"][t]

    # get existing GitHub branches:
    existing_github_branches = getGHBranches(github_token)

    for exporter_name, exporter_config in work.items():

        # first we need to work out the context for this exporter:
        context = exporter_config["context"]["static"]

        exporter_url = context["URL"]
        exporter_current_version = context["version"]

        logging.info(
            "Checking updates for %s" % (exporter_name.upper().replace("_", " "))
        )
        # get latest exporter release:
        (
            exporter_latest_version,
            exporter_release_notes,
            exporter_url,
        ) = getLatestGHReleaseVersion(github_token, exporter_name, exporter_url)
        logging.info(
            "%s: current version: %s, latest version %s"
            % (exporter_name, exporter_current_version, exporter_latest_version)
        )

        # check if we are already on latest version:
        if exporter_current_version != exporter_latest_version:
            github_branch = "%s_%s" % (
                exporter_name,
                exporter_latest_version.replace(".", "_"),
            )

            # check if there is already existing PR for this update:
            if github_branch not in existing_github_branches:
                logging.info(
                    "Updating %s: %s -> %s"
                    % (exporter_name, exporter_current_version, exporter_latest_version)
                )

                # update package version:
                config["packages"][exporter_name]["context"]["static"][
                    "version"
                ] = exporter_latest_version

                github_commit_message = "Update %s from %s to %s" % (
                    exporter_name,
                    exporter_current_version,
                    exporter_latest_version,
                )
                if not check_mode:
                    updateGHTemplate(
                        github_token,
                        template_config,
                        github_branch,
                        github_commit_message,
                        config,
                        exporter_release_notes,
                        exporter_url,
                    )

                # exit so that there is exactly one update present in PR:
                sys.exit(0)
            else:
                logging.info(
                    "Branch '%s' is already present, not pushing updates"
                    % github_branch
                )
