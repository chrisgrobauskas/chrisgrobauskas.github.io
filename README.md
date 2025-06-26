# chrisgrobauskas.github.io
Purpose: personal site repository

The `./AI.md` in this site has more details around the site for style and guidelines.

MkDocs is used to preprocess `./docs` files into a static html blog. To get a local environment you can install python 3.x and follow the instructions below.

## Local Development

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Serve the site locally with MkDocs:**
    ```bash
    mkdocs serve -a localhost:8080
    ```
    This will start a local server, usually at [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Publishing with GitHub Actions

Site deployment is automated using a GitHub Actions workflow defined in `.github/workflows/publish.yml`. The workflow is triggered on pushes to the `main` or `master` branches, or manually via the GitHub UI.

> This site is older and the main branch is named `master`.

**Workflow steps:**
1. **Checkout code:** Uses the latest code from the repository.
2. **Set up Python:** Installs Python 3.x for the build environment.
3. **Install dependencies:** Installs all required Python packages from `requirements.txt`.
4. **Build site:** Runs `mkdocs build` to generate the static site in the `./site` directory.
5. **Add CNAME:** Copies the `CNAME` file (for custom domains) into the build output.
6. **Configure GitHub Pages:** Prepares the environment for deployment.
7. **Upload artifacts:** Uploads the built site as an artifact for deployment.
8. **Deploy:** Publishes the site to GitHub Pages.

No manual deployment is needed—just push to `main` or `master` and the site will be rebuilt and published automatically.