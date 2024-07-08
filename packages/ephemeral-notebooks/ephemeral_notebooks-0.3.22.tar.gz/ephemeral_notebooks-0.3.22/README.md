# Urlify

## A JupyterLab Extension for Sharing Notebooks via URL

Urlify is a JupyterLab extension that allows you to easily share your Jupyter notebooks by encoding their content into a URL. This enables quick sharing and collaboration without the need for file transfers or cloud storage.

## Features

- **Save to URL**: Compress and encode your notebook content into a shareable URL with a single click.
- **Configurable Settings**: Choose whether to include cell outputs and select the appropriate URL path for your Jupyter environment.
- **Easy Sharing**: The generated URL is automatically copied to your clipboard for immediate sharing.

## Installation

To install the extension, run the following command in your environment:

```
pip install urlify
```

If you are [deploying your own jupyterlite instance](https://github.com/jupyterlite/demo), you can install urlify by adding it to your requirements.

## Usage

1. Open a Jupyter notebook in JupyterLab.
2. Look for the "Save to URL" button in the notebook toolbar.
3. Click the main button to save the current content of your notebook to a URL.
4. Use the settings icon (gear) next to the main button to configure options:
   - Toggle including cell outputs
   - Select the appropriate URL path for your Jupyter environment
5. Share the generated URL with your colleagues or students.

## Configuration

The extension provides two main configuration options:

1. **Copy Notebook Output**: When enabled, cell outputs are included in the generated URL. This is disabled by default to keep URLs shorter but will require the recipient to run the notebook to see the outputs. Modern notebook
2. **URL Path**: Choose the appropriate path based on your Jupyter environment:
   - `/lab/index.html` for JupyterLab
   - `/retro/notebooks/index.html` for Jupyter Notebook

## Inspiration

This project draws inspiration from the Vega Editor's "Save to URL" feature and PyCafe's goal to simplify sharing python data apps. We've adapted these ideas to the Jupyter ecosystem, aiming to make notebook sharing as easy as passing along a URL. While our approach differs, we're all working towards making collaboration in the coding world more accessible. We encourage you to check out these awesome projects too: Vega Editor (https://vega.github.io/editor/) and PyCafe (https://py.cafe/).

## Contributing

We don't have a formal contributing process right now, but we're open to feedback and suggestions. Feel free to open an issue or reach out to us directly if you have any ideas or improvements in mind.

## License

This project is licensed under the BSD-3-Clause License. See the [LICENSE](LICENSE) file for details.