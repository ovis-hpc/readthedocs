# Documentation

Edits should be made to the `.rst` files.
The documentation can be built with `make html` or `make man`.
The generated files will be found in the `_build` directory.

## Manual Development Container

To generate the container manually, build it with:

```bash
$ docker build -f ./.devcontainer/Dockerfile -t ovis-docs .
```
This will build the base environment. You can then bind your container to the present
working directory to build:

```bash
$ docker run -it --rm -v $PWD/:/workspace/ovis-docs ovis-docs make html
```

You can also go in interactively - just be careful and don't commit from within the container.

```bash
$ docker run -it --rm -v $PWD/:/workspace/ovis-docs ovis-docs bash
```

### If Using a Machine with a Proxy

If you are working in an environment with a proxy, you may need to configure the proxy settings inside the Docker container in order to build the documentation properly.

Uncomment the following lines (or add them if they don't exist) in the conf.py code:

```python
os.environ["CURL_CA_BUNDLE"] = '/etc/ssl/certs/ca-bundle.crt'
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-bundle.crt'
```

Run the following command to build the documentation using the proxy. Make sure to replace `<path-to-certs>` with the actual path to the certificates on your machine, and `<proxy:port>` with your proxy's address and port:

```bash
$ docker run -u root -it --rm -v $PWD/:/workspace/ovis-docs -v /<path-to-certs>:/etc/ssl/certs/ -e http_proxy=http://<proxy:port> -e https_proxy=<proxy:port> ovis-docs make html
```
This ensures that the Docker container has access to the necessary certificates and can connect through the proxy to download dependencies or access external resources.


### Steps to visualize changes on Read the Docs:
1. **Fork the repository**: Fork the repository where the docs are located to your own GitHub account.
2. **Create a Read the Docs account**: Sign up for a free Read the Docs account at [readthedocs.org](https://readthedocs.org/).
3. **Link the repository**: 
    - After logging in, go to the **"Import a Project"** page on [Read the Docs](https://readthedocs.org/projects/).
    - Choose **"GitHub"** as the source and authorize Read the Docs to access your GitHub account.
    - Select your forked repository from the list.
4. **Specify the correct branch**: 
    - In the project settings, you will be asked to specify the branch of your repository. Select the branch that contains the changes you've made to the documentation.
5. **Set the location of `.readthedocs.yml`**: 
    - Read the Docs will need to know where your `.readthedocs.yml` file is located. In the project settings, ensure that you specify the **current directory** (`./`) as the location of the `.readthedocs.yml` file.
    - The `.readthedocs.yml` file controls the configuration of your documentation build process on Read the Docs (including things like Python dependencies, versioning, and build steps).
6. **Build the documentation**: After linking the project and selecting the correct branch, Read the Docs will automatically build the documentation. You can view the generated docs at the provided URL.

This will allow you to see your changes in real-time as you push updates to the branch.

## Installing Sphinx

Sphinx is used to generate man pages from the `.rst` files.
If Sphinx is not installed on the system, the following may be used to install Sphinx and the required theme.

``` shell
pip install -r requirements.txt
```

Users may want to install these packages into a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html)

## Release

SPDX-License-Identifier: LGPL-3.0

LLNL-CODE-764420
