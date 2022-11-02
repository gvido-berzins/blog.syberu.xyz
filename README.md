## blog.syberu.xyz

This repository is used as a backup, an maybe an example of utilizing pelican
and showing an example of managing such publishing process.

## Tags

I use `notes` and `blog` tags as main categories.

- `notes` - short articles about a single thing
- `blog` - a blog or a write-up

## Theme

- [pelican-twitchy](https://github.com/ingwinlu/pelican-twitchy/)

## Publishing

For publishing I use a custom script `sync.py` which simply runs rsync to
synchornize all my generated pelican output with the server it's hosted on.

Commands:

```bash
# Before publishing
cd blog/
make clean && make html

# Uploading ready blog folder
python sync.py up

# Download blog folder from the site
python sync.py down
```

## Writing

At the moment, my workflow is like this.

Scenario 1:

1. Randomly come up with an idea.
2. "I can write about this."
3. Write something

Scenario 2:

1. Start learning something.
2. Take notes.
3. Check for secrets.
4. Publish notes.

Scenario 3:

1. Taking notes or struggle with a problem.
2. "I can turn this into a blog."
3. Write a blog.

## Hosting

My websites are hosted on a VPS (service - vultr.com) which I manage.

## Development

Prepare the development environment:

```bash
# Python dependencies
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Install dependencies for publishing (Arch Linux)
make deps
```

Run a local development server:

```bash
cd blog/
make clean && make html
pelican --autoreload --listen
```

### Adding images

Images are added in `blog/content/images` and can be referenced by the following
sytax `![Alt image name for screen readers](images/image.png){: .image-process-crisp}`

- The `{: .image-process-crisp}` makes sure images are the same length and are responsive.
