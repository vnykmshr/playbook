# Deployment Guide

## Publishing to GitHub Pages

The Engineering Playbook documentation is automatically deployed to GitHub Pages using GitHub Actions.

### How It Works

1. **Push to main** → GitHub Actions workflow triggers
2. **Build** → mkdocs builds HTML from markdown in `docs/`
3. **Deploy** → Site published to `gh-pages` branch
4. **Live** → Available at `https://username.github.io/playbook/`

### GitHub Pages Configuration

Enable GitHub Pages for this repository:

1. Go to **Settings** → **Pages**
2. Select **Deploy from a branch**
3. Choose **gh-pages** branch
4. Select **/ (root)** folder
5. Click **Save**

The workflow automatically creates/updates the `gh-pages` branch on every push to main.

### Local Development

Build and test locally before pushing:

```bash
# Install mkdocs and material theme
pip install mkdocs mkdocs-material

# Build the site
mkdocs build        # Output in site/

# Serve locally
mkdocs serve        # Live at http://localhost:8000
```

### Site Structure

- **Source**: `docs/` (markdown files)
- **Config**: `mkdocs.yml`
- **Build output**: `site/` (git-ignored, generated)
- **Deploy**: `.github/workflows/deploy-docs.yml`

### What Triggers Deployment

The workflow only runs when:
- Changes pushed to **main** branch
- Changes affect `docs/`, `mkdocs.yml`, or the workflow itself

This prevents unnecessary builds for unrelated changes.

### Custom Domain

To use a custom domain (e.g., playbook.dev):

1. Add file: `docs/CNAME` with domain:
```
playbook.dev
```

2. Update GitHub Pages Settings:
   - Go to **Settings** → **Pages**
   - Enter custom domain
   - GitHub creates DNS check

3. Update DNS records (your registrar):
```
CNAME playbook.dev username.github.io
```

### Troubleshooting

**Build fails?**
- Check workflow logs: **Actions** tab
- Verify `mkdocs.yml` syntax
- Ensure all referenced docs exist

**Site doesn't update?**
- Workflow only runs on pushes to **main**
- Check Actions tab to see workflow status
- Hard refresh browser (Cmd+Shift+R)

**404 errors?**
- Check `mkdocs.yml` navigation
- Verify file names in `docs/` match references
- Build locally with `mkdocs build` to verify

### Documentation

- **Build locally**: `mkdocs serve`
- **Theme docs**: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- **MkDocs docs**: [MkDocs](https://www.mkdocs.org/)

---

**Note**: Do NOT commit the `site/` directory. It's automatically generated and deployed by GitHub Actions.
