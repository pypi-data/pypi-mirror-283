import * as LZString from 'lz-string';
import { NotebookModel } from '@jupyterlab/notebook';
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';
import { UUID } from '@lumino/coreutils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ToolbarButton, Dialog, showDialog } from '@jupyterlab/apputils';
import { Clipboard } from '@jupyterlab/apputils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { Widget } from '@lumino/widgets';

let savedParams: URLSearchParams | null = null;

// Save the URL parameters on page load
function saveUrlParameters(): void {
  const urlParams = new URLSearchParams(window.location.hash.slice(1));
  savedParams = urlParams;
  console.log('Saved URL parameters:', savedParams.toString());
}

// Decompress the saved URL parameter and load notebook content
function decompressSavedContent(): any | null {
  if (savedParams) {
    const compressedContent = savedParams.get('notebook');
    if (compressedContent) {
      const decompressedContent =
        LZString.decompressFromEncodedURIComponent(compressedContent);
      const content = JSON.parse(decompressedContent);
      console.log('decompressedContent', content);
      return content;
    }
  }
  return null;
}

// Add a route to render the temporary notebook
function addTempNotebookRoute(
  app: JupyterFrontEnd,
  filebrowserFactory: IFileBrowserFactory,
  router: IRouter
): void {
  if (router) {
    app.commands.addCommand('notebook:start-nav', {
      label: 'Open Temp Notebook from URL',
      execute: async args => {
        const { request } = args as IRouter.ILocation;
        const url = new URL(`http://example.com${request}`);
        const params = url.searchParams;
        const isTempNotebook = params.get('tempNotebook');

        const createFromURLRoute = async () => {
          router.routed.disconnect(createFromURLRoute);
          if (isTempNotebook && isTempNotebook == '1') {
            await app.commands.execute('notebook:open-temp', {});
          }
        };

        router.routed.connect(createFromURLRoute);
      }
    });

    app.commands.addCommand('notebook:open-temp', {
      label: 'Open Temporary Notebook',
      execute: async args => {
        const createNew = async (
          cwd: string,
          kernelId: string,
          kernelName: string
        ) => {
          const model = await app.commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'notebook'
          });

          if (model !== undefined) {
            const widget = await app.commands.execute('docmanager:open', {
              path: model.path,
              factory: 'Notebook',
              kernel: { id: kernelId, name: kernelName }
            });

            widget.isUntitled = true;
            const tempId = `temp-notebook-${UUID.uuid4()}`;
            await widget.context.rename(tempId + '.ipynb');

            const content = decompressSavedContent();
            if (content) {
              const notebookModel = widget.context.model as NotebookModel;
              notebookModel.fromJSON(content);
              await widget.context.save();
            }

            return widget;
          }
        };

        //@ts-ignore
        const currentBrowser = filebrowserFactory?.tracker.currentWidget ?? filebrowserFactory.defaultBrowser;
        const cwd = (args['cwd'] as string) || (currentBrowser?.model.path ?? '');
        const kernelId = (args['kernelId'] as string) || '';
        const kernelName = (args['kernelName'] as string) || '';

        await createNew(cwd, kernelId, kernelName);
      }
    });
  }
}

// Compress the notebook text, set as URL parameter, and copy to clipboard
async function compressNotebookContent(notebookPanel: any, settings: { copyOutput: boolean, urlPath: string }) {
  let notebookContent: any = notebookPanel.context.model.toJSON();

  if (!settings.copyOutput) {
    notebookContent.cells = notebookContent.cells.map((cell: any) => {
      if (cell.cell_type === 'code') {
        cell.outputs = [];
        cell.execution_count = null;
      }
      return cell;
    });
  }

  const stringContent = JSON.stringify(notebookContent);

  if (stringContent.length > 10000) {
    const result = await showDialog({
      title: 'Large Notebook',
      body: 'The notebook content exceeds 10,000 characters. Do you want to continue with the full content or copy only inputs?',
      buttons: [
        Dialog.cancelButton(),
        Dialog.okButton({ label: 'Full Content' }),
        Dialog.okButton({ label: 'Inputs Only' })
      ]
    });

    if (result.button.label === 'Inputs Only') {
      notebookContent.cells = notebookContent.cells.map((cell: any) => {
        if (cell.cell_type === 'code') {
          cell.outputs = [];
          cell.execution_count = null;
        }
        return cell;
      });
    } else if (result.button.accept === false) {
      return; // User cancelled
    }
  }

  const compressedContent = LZString.compressToEncodedURIComponent(JSON.stringify(notebookContent));

  // Create a URL object from the current location
  const url = new URL(window.location.href);

  // Update the URL path based on the selected setting
  url.pathname = settings.urlPath;

  // Add the hash and query parameters
  url.hash = `notebook=${compressedContent}`;
  url.searchParams.set('tempNotebook', '1');
  url.searchParams.set('path', 'temp.ipynb');
  console.log('new url', url.toString());

  const newUrl = url.toString();
  Clipboard.copyToSystem(newUrl);
}

class SettingsDialog extends Widget {
  constructor(
    private onSave: (settings: { copyOutput: boolean; urlPath: string }) => void,
    private initialSettings: { copyOutput: boolean; urlPath: string }
  ) {
    super();
    this.buildDialog();
  }

  private buildDialog() {
    const container = document.createElement('div');
    container.style.padding = '15px';

    const titleEl = document.createElement('h2');
    titleEl.textContent = 'Settings';
    container.appendChild(titleEl);

    const copyOutputLabel = document.createElement('label');
    copyOutputLabel.style.display = 'block';
    copyOutputLabel.style.marginBottom = '10px';
    const copyOutputCheckbox = document.createElement('input');
    copyOutputCheckbox.type = 'checkbox';
    copyOutputCheckbox.checked = this.initialSettings.copyOutput;
    copyOutputLabel.appendChild(copyOutputCheckbox);
    copyOutputLabel.appendChild(document.createTextNode(' Copy notebook output'));
    container.appendChild(copyOutputLabel);

    const urlPathLabel = document.createElement('label');
    urlPathLabel.style.display = 'block';
    urlPathLabel.style.marginBottom = '10px';
    urlPathLabel.textContent = 'URL path: ';
    const urlPathSelect = document.createElement('select');
    const paths = ['/lab/index.html', '/retro/notebooks/index.html', '/tree/index.html'];
    paths.forEach(path => {
      const option = document.createElement('option');
      option.value = path;
      option.textContent = path;
      if (path === this.initialSettings.urlPath) {
        option.selected = true;
      }
      urlPathSelect.appendChild(option);
    });
    urlPathLabel.appendChild(urlPathSelect);
    container.appendChild(urlPathLabel);

    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.onclick = () => {
      this.onSave({
        copyOutput: copyOutputCheckbox.checked,
        urlPath: urlPathSelect.value
      });
    };
    container.appendChild(saveButton);

    this.node.appendChild(container);
  }
}

// Add "Save to URL" dropdown button to the notebook toolbar
function addSaveToUrlButton(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker
) {
  let settings = {
    copyOutput: false,
    urlPath: '/lab/index.html'
  };

  const saveToUrlButton = new ToolbarButton({
    label: 'Save to URL',
    onClick: () => {
      const current = notebookTracker.currentWidget;
      if (current) {
        compressNotebookContent(current, settings);
      }
    },
    tooltip: 'Save notebook content to URL and copy to clipboard'
  });

  const settingsButton = new ToolbarButton({
    icon: 'ui-components:settings',
    onClick: () => {
      const dialog = new SettingsDialog(
        (newSettings) => {
          settings = newSettings;
          dialog.dispose();
        },
        settings
      );

      showDialog({
        title: 'Save to URL Settings',
        body: dialog,
        buttons: [Dialog.cancelButton()]
      });
    },
    tooltip: 'Save to URL Settings'
  });

  const container = document.createElement('div');
  container.classList.add('jp-SplitButton');
  container.appendChild(saveToUrlButton.node);
  container.appendChild(settingsButton.node);

  notebookTracker.widgetAdded.connect((sender, panel) => {
    panel.toolbar.insertItem(10, 'saveToUrl', container);
  });
}

const extension: JupyterFrontEndPlugin<void> = {
  id: 'urlify-nb',
  autoStart: true,
  requires: [IFileBrowserFactory, IRouter, INotebookTracker],
  activate: async (
    app: JupyterFrontEnd,
    filebrowserFactory: IFileBrowserFactory,
    router: IRouter,
    notebookTracker: INotebookTracker
  ) => {
    try {
      console.log('Activating ephemeral-notebooks extension');

      router.register({
        command: 'notebook:start-nav',
        pattern: /(tempNotebook=1)/,
        rank: 20
      });

      addSaveToUrlButton(app, notebookTracker);
      saveUrlParameters();
      await addTempNotebookRoute(app, filebrowserFactory, router);

      console.log('ephemeral-notebooks extension activated successfully');
    } catch (error) {
      console.error('Error activating ephemeral-notebooks extension:', error);
    }
  }
};

export default extension;