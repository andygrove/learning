#!/usr/bin/env python3
"""
Publish the Spark Reference website.

Builds the MkDocs site and deploys to the web server.
"""

import os
import subprocess
import sys


def run_command(cmd, cwd=None):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        sys.exit(1)


def main():
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Build the MkDocs site
    print("\n=== Building MkDocs site ===")
    run_command(['mkdocs', 'build'], cwd=script_dir)

    # Step 2: Deploy
    print("\n=== Deploying to website ===")

    # Create tarball in script dir (not inside site/) to avoid "file changed" error
    tgz_path = os.path.join(script_dir, 'sparkreference.tgz')
    run_command(['tar', 'czf', tgz_path, '-C', 'site', '.'], cwd=script_dir)

    ssh_key = os.path.expanduser('~/.ssh/id_rsa_lightsail.pem')
    server = 'ubuntu@18.188.179.245'

    # Copy tarball to server
    run_command(['scp', '-i', ssh_key, tgz_path, f'{server}:'])

    # Extract on server
    run_command([
        'ssh', '-i', ssh_key, server,
        'cd /var/www/sparkreference.io ; tar xzf /home/ubuntu/sparkreference.tgz'
    ])

    # Cleanup local tarball
    os.remove(tgz_path)

    print("\n=== Deployment complete ===")


if __name__ == "__main__":
    main()
