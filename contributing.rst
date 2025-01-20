.. _contributing:

============
Contributing
============

The OVIS-HPC team values contributions of all kinds: bug fixes, new features, documentation, and more. If you have questions or need help, please `contact us <https://github.com/ovis-hpc/OVIS-HPC/people>`_.

This guide explains how to contribute to `OVIS-HPC projects <https://github.com/ovis-hpc>`_ efficiently.

.. _pull-requests:

-------------
Pull Requests
-------------

Pull requests are how changes are made to OVIS-HPC projects. We use GitHub’s
`fork and pull <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-collaborative-development-models>`_
model. Contributors create branches in their own forks and submit pull requests to propose changes.

Steps to create a pull request:

1. `Fork <https://help.github.com/en/github/getting-started-with-github/fork-a-repo>`_ the repository.
2. Clone your fork: ``git clone git@github.com:[username]/ovis-hpc/[project].git``
3. Create a feature branch: ``git checkout -b new_feature``
4. Make your changes and add tests if needed.
5. Run ``make check`` to ensure everything works.
6. Organize your commits into logical units.
7. Push your branch: ``git push origin new_feature``
8. Open a pull request to the `ovis-hpc/[project]` repository. Include a description of the changes and reference related issues.
9. Automated tests will run on your pull request.

For significant changes, open an issue first to discuss your ideas.

Pull requests to the main branch should be rebased to avoid merge commits. Use `WIP:` in the title for drafts to prevent premature merging.

.. _dev-guidelines:

--------------------
Developer Guidelines
--------------------

Follow these guidelines for contributing:

* Check existing issues and pull requests to avoid duplication.
* Include tests when possible. Automated coverage reports are generated for pull requests.
* Update documentation as needed. If you can’t, open a `documentation issue <https://github.com/ovis-hpc/docs/issues>`_.
* Write clear, focused commits:

  - Avoid merge commits.
  - Keep refactoring, new features, and fixes in separate commits.
  - Use meaningful commit titles with a prefix indicating the area (e.g., ``sos:``, ``maestro:``, ``baler:``, ``ldms:``).
  - Reference related issues in the commit message.
  - Use clear, imperative phrasing and wrap lines at 72 characters.

