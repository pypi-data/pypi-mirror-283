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

import {settingsIcon} from '@jupyterlab/ui-components';

console.log('in outside new');
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

            updateUrlWithNotebookPath(widget.context.path);
            function updateUrlWithNotebookPath(notebookPath: string) {
              const url = new URL(window.location.href);
            
              // Get the current URL
              const currentUrl = window.location.href;
        
        
              // Extract the base URL up to /lab/index.html
              const baseUrlMatch = currentUrl.match(/(.*\/)lab\/index\.html/);
              const baseUrl = baseUrlMatch ? baseUrlMatch[1] : '';
        
              //Jupyterlite
              let retroView = baseUrl + `notebooks/index.html?path=${notebookPath}&${notebookPath}&${url.search}&${url.hash}`;
              window.location.href = retroView
            }

            
          
          

            return widget;
          }
        };

        //@ts-ignore
        const currentBrowser = filebrowserFactory?.tracker.currentWidget ?? filebrowserFactory.defaultBrowser;
        const cwd =
          (args['cwd'] as string) || (currentBrowser?.model.path ?? '');
        const kernelId = (args['kernelId'] as string) || '';
        const kernelName = (args['kernelName'] as string) || '';

        await createNew(cwd, kernelId, kernelName);
      }
    });
  }
}

// Compress the notebook text, set as URL parameter, and copy to clipboard
async function compressNotebookContent(
  notebookPanel: any,
  settings: { copyOutput: boolean; urlPath: string }
) {
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

  const compressedContent = LZString.compressToEncodedURIComponent(
    JSON.stringify(notebookContent)
  );

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
    private onSettingsChange: (settings: {
      copyOutput: boolean;
      openAsNotebook: boolean;
      urlPath: string;
    }) => void,
    private initialSettings: {
      copyOutput: boolean;
      openAsNotebook: boolean;
      urlPath: string;
    }
  ) {
    super();
    this.buildDialog();
  }

  private buildDialog() {
    const container = document.createElement('div');
    container.style.padding = '15px';

    // Copy Output Switch
    const copyOutputLabel = this.createSwitchControl(
      'Copy notebook output',
      this.initialSettings.copyOutput,
      (checked) => this.updateSettings({ copyOutput: checked })
    );
    container.appendChild(copyOutputLabel);

    // Open as Notebook Switch
    const openAsNotebookLabel = this.createSwitchControl(
      'Open as notebook',
      this.initialSettings.openAsNotebook,
      (checked) => this.updateSettings({ openAsNotebook: checked })
    );
    container.appendChild(openAsNotebookLabel);

    // URL Path Selection
    const urlPathLabel = document.createElement('label');
    urlPathLabel.style.display = 'block';
    urlPathLabel.style.marginBottom = '10px';
    urlPathLabel.textContent = 'URL path: ';
    const urlPathSelect = document.createElement('select');
    urlPathSelect.style.width = '100%';
    urlPathSelect.style.marginBottom = '10px';

    const baseUrl = window.location.href.split('/lab')[0];
    const paths = [
      { label: 'JupyterLite', value: '/jupyterlite/lab/index.html' },
      { label: 'JupyterLab', value: '/lab/index.html' },
      { label: 'Custom', value: 'custom' }
    ];

    paths.forEach(path => {
      const option = document.createElement('option');
      option.value = path.value;
      option.textContent = `${path.label}${path.value !== 'custom' ? ` (${baseUrl}${path.value})` : ''}`;
      if (path.value === this.initialSettings.urlPath) {
        option.selected = true;
      }
      urlPathSelect.appendChild(option);
    });

    urlPathLabel.appendChild(urlPathSelect);
    container.appendChild(urlPathLabel);

    // Custom URL input (initially hidden)
    const customUrlInput = document.createElement('input');
    customUrlInput.type = 'text';
    customUrlInput.placeholder = 'Enter custom URL path';
    customUrlInput.style.width = '100%';
    customUrlInput.style.marginBottom = '10px';
    customUrlInput.style.display = 'none';
    container.appendChild(customUrlInput);

    // Warning message for custom URL (initially hidden)
    const warningMessage = document.createElement('p');
    warningMessage.textContent = 'Reminder: urlify must be installed on the Jupyter instance for custom URLs.';
    warningMessage.style.color = 'orange';
    warningMessage.style.display = 'none';
    container.appendChild(warningMessage);

    // Event listener for URL path selection
    urlPathSelect.addEventListener('change', () => {
      if (urlPathSelect.value === 'custom') {
        customUrlInput.style.display = 'block';
        warningMessage.style.display = 'block';
      } else {
        customUrlInput.style.display = 'none';
        warningMessage.style.display = 'none';
        this.updateSettings({ urlPath: urlPathSelect.value });
      }
    });

    // Event listener for custom URL input
    customUrlInput.addEventListener('input', () => {
      this.updateSettings({ urlPath: customUrlInput.value });
    });

    this.node.appendChild(container);
  }

  private createSwitchControl(label: string, initialState: boolean, onChange: (checked: boolean) => void) {
    const container = document.createElement('label');
    container.style.display = 'flex';
    container.style.alignItems = 'center';
    container.style.marginBottom = '10px';
    container.style.cursor = 'pointer';

    const switchElem = document.createElement('div');
    switchElem.style.width = '40px';
    switchElem.style.height = '20px';
    switchElem.style.backgroundColor = initialState ? '#4CAF50' : '#ccc';
    switchElem.style.borderRadius = '10px';
    switchElem.style.position = 'relative';
    switchElem.style.transition = 'background-color 0.3s';
    switchElem.style.marginRight = '10px';

    const switchHandle = document.createElement('div');
    switchHandle.style.width = '18px';
    switchHandle.style.height = '18px';
    switchHandle.style.backgroundColor = 'white';
    switchHandle.style.borderRadius = '50%';
    switchHandle.style.position = 'absolute';
    switchHandle.style.top = '1px';
    switchHandle.style.left = initialState ? '21px' : '1px';
    switchHandle.style.transition = 'left 0.3s';

    switchElem.appendChild(switchHandle);
    container.appendChild(switchElem);
    container.appendChild(document.createTextNode(label));

    container.addEventListener('click', () => {
      const newState = switchHandle.style.left === '1px';
      switchHandle.style.left = newState ? '21px' : '1px';
      switchElem.style.backgroundColor = newState ? '#4CAF50' : '#ccc';
      onChange(newState);
    });

    return container;
  }

  private updateSettings(newSettings: Partial<{ copyOutput: boolean; openAsNotebook: boolean; urlPath: string }>) {
    this.onSettingsChange({
      ...this.initialSettings,
      ...newSettings
    });
  }
}

// Add "Save to URL" dropdown button to the notebook toolbar
function addSaveToUrlButton(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker
) {
  
  let settings = {
    copyOutput: false, openAsNotebook: true, urlPath:'/lab/index.html'
  };

  const saveToUrlButton = new ToolbarButton({
    label: 'Save to url',
    onClick: () => {
      const current = notebookTracker.currentWidget;
      console.log('in press', current, settings);
      if (current) {
        compressNotebookContent(current, settings);
      }
    },
    tooltip: 'Save notebook content to URL and copy to clipboard'
  });

  const settingsButton = new ToolbarButton({
    icon: settingsIcon,
    //label: 'setting',
    onClick: () => {
      const dialog = new SettingsDialog(newSettings => {
        settings = newSettings;
        dialog.dispose();
      }, settings);

      showDialog({
        title: 'Save to URL Settings',
        body: dialog,
        buttons: [Dialog.cancelButton()]
      });
    },
    tooltip: 'Save to URL Settings'
  });
  
  notebookTracker.widgetAdded.connect((sender, panel) => {
    console.log('added',saveToUrlButton, settingsButton, panel.toolbar)

    panel.toolbar.insertItem(10, 'saveToUrl', saveToUrlButton);
    panel.toolbar.insertItem(11, 'settingsButton', settingsButton);

  });

  

  //   // Main widget to hold the split button functionality
  // class SplitButtonWidget extends Widget {
  //     constructor() {
  //       super({ node: document.createElement('div') })
  //       console.log('creating split button', this, this.node)
  //       this.addClass('jp-SplitButton');
  //       this.node.appendChild(settingsButton.node);
  //       this.node.appendChild(saveToUrlButton.node);

  //     }
  //   }

  

  //   // Usage in a notebook tracker
  //     notebookTracker.widgetAdded.connect((sender, panel) => {
  //         const splitButton = new SplitButtonWidget();
  //         panel.toolbar.insertItem(10, 'saveToUrl', splitButton);
  //     });
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
      console.log('Activating ephemeral-notebooks extension: new');

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
