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

            if(settings.openAsNotebook){

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
  private settings: {
    copyOutput: boolean;
    urlPath: string;
    openAsNotebook: boolean;
  };
  private newSettings: {
    copyOutput: boolean;
    urlPath: string;
    openAsNotebook: boolean;
  };
  private container: HTMLDivElement;
  //@ts-ignore
  private saveButton: HTMLButtonElement;

  constructor(
    private onSettingsChange: (settings: {
      copyOutput: boolean;
      urlPath: string;
      openAsNotebook: boolean;
    }) => void,
    initialSettings: {
      copyOutput: boolean;
      urlPath: string;
      openAsNotebook: boolean;
    }
  ) {
    super();
    this.settings = { ...initialSettings };
    this.newSettings = { ...initialSettings };
    this.container = document.createElement('div');
    this.node.appendChild(this.container);
    this.buildDialog();
  }

  private buildDialog() {
    console.log('Building dialog with settings:', this.settings);
    this.container.innerHTML = ''; // Clear existing content
    this.container.style.padding = '15px';
    this.container.style.minWidth = '300px';

    // Copy Output Switch
    const copyOutputSwitch = this.createSwitchControl(
      'Copy notebook output',
      this.newSettings.copyOutput,
      (checked) => this.updateNewSettings({ copyOutput: checked })
    );
    this.container.appendChild(copyOutputSwitch);

    // URL Path Selection
    const urlPathLabel = document.createElement('label');
    urlPathLabel.style.display = 'block';
    urlPathLabel.style.marginTop = '15px';
    urlPathLabel.style.marginBottom = '5px';
    urlPathLabel.textContent = 'URL path:';
    this.container.appendChild(urlPathLabel);

    const urlPathSelect = document.createElement('select');
    urlPathSelect.style.width = '100%';
    urlPathSelect.style.padding = '5px';
    urlPathSelect.style.marginBottom = '10px';

    const paths = [
      { label: 'JupyterLite', value: '/jupyterlite/lab/index.html', openAsNotebook: false },
      { label: 'JupyterLite Notebook', value: '/jupyterlite/notebooks/index.html', openAsNotebook: true },
      { label: 'JupyterLab', value: '/lab/index.html', openAsNotebook: false },
      { label: 'Custom', value: 'custom', openAsNotebook: false }
    ];

    paths.forEach(path => {
      const option = document.createElement('option');
      option.value = JSON.stringify(path);
      option.textContent = path.label;
      if (path.value === this.newSettings.urlPath && path.openAsNotebook === this.newSettings.openAsNotebook) {
        option.selected = true;
      }
      urlPathSelect.appendChild(option);
    });

    this.container.appendChild(urlPathSelect);

    // URL display
    const urlDisplay = document.createElement('p');
    urlDisplay.style.fontSize = '0.9em';
    urlDisplay.style.color = '#666';
    urlDisplay.style.marginTop = '5px';
    urlDisplay.style.wordBreak = 'break-all';
    this.container.appendChild(urlDisplay);

    // Custom URL input (initially hidden)
    const customUrlInput = document.createElement('input');
    customUrlInput.type = 'text';
    customUrlInput.placeholder = 'Enter custom URL path';
    customUrlInput.style.width = '100%';
    customUrlInput.style.padding = '5px';
    customUrlInput.style.marginTop = '10px';
    customUrlInput.style.display = 'none';
    this.container.appendChild(customUrlInput);

    // Warning message for custom URL (initially hidden)
    const warningMessage = document.createElement('p');
    warningMessage.textContent = 'Warning: urlify must be installed on the Jupyter instance for custom URLs.';
    warningMessage.style.color = 'orange';
    warningMessage.style.fontSize = '0.9em';
    warningMessage.style.display = 'none';
    this.container.appendChild(warningMessage);

    // Event listener for URL path selection
    urlPathSelect.addEventListener('change', () => {
      console.log('URL path changed');
      const selectedOption = JSON.parse(urlPathSelect.value);
      if (selectedOption.value === 'custom') {
        customUrlInput.style.display = 'block';
        warningMessage.style.display = 'block';
        urlDisplay.textContent = '';
      } else {
        customUrlInput.style.display = 'none';
        warningMessage.style.display = 'none';
        this.updateNewSettings({ 
          urlPath: selectedOption.value, 
          openAsNotebook: selectedOption.openAsNotebook 
        });
        this.updateUrlDisplay(urlDisplay, selectedOption.value);
      }
    });

    // Event listener for custom URL input
    customUrlInput.addEventListener('input', () => {
      console.log('Custom URL input changed');
      this.updateNewSettings({ urlPath: customUrlInput.value, openAsNotebook: false });
      this.updateUrlDisplay(urlDisplay, customUrlInput.value);
    });

    // Initial URL display update
    this.updateUrlDisplay(urlDisplay, this.newSettings.urlPath);

    // Save Button
    this.saveButton = document.createElement('button');
    this.saveButton.textContent = 'Save';
    this.saveButton.style.marginTop = '15px';
    this.saveButton.style.padding = '5px 10px';
    this.saveButton.disabled = true;
    this.saveButton.addEventListener('click', () => this.saveSettings());
    this.container.appendChild(this.saveButton);

    console.log('Dialog built successfully');
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

  private updateNewSettings(partialSettings: Partial<{ copyOutput: boolean; urlPath: string; openAsNotebook: boolean }>) {
    this.newSettings = { ...this.newSettings, ...partialSettings };
    this.updateSaveButtonState();
  }

  private updateSaveButtonState() {
    const hasChanges = JSON.stringify(this.settings) !== JSON.stringify(this.newSettings);
    this.saveButton.disabled = !hasChanges;
    this.saveButton.style.backgroundColor = hasChanges ? '#4CAF50' : '#ccc';
    this.saveButton.style.color = hasChanges ? 'white' : 'black';
    this.saveButton.style.cursor = hasChanges ? 'pointer' : 'default';
  }

  private saveSettings() {
    console.log('Saving settings:', this.newSettings);
    this.settings = { ...this.newSettings };
    this.onSettingsChange(this.settings);
    this.updateSaveButtonState();
    console.log('Settings saved:', this.settings);
  }

  private updateUrlDisplay(element: HTMLElement, urlPath: string) {
    const baseUrl = window.location.href.split('/lab')[0];
    element.textContent = `Links to: ${baseUrl}${urlPath}`;
    console.log('URL display updated:', element.textContent);
  }
}

let settings = {
  copyOutput: false, openAsNotebook: true, urlPath:'/lab/index.html'
};


// class SplitButton extends Widget {
//   constructor(
//     private saveAction: () => void,
//     private settingsAction: () => void
//   ) {
//     super();
//     this.addClass('jp-SplitButton');
//     this.buildWidget();
//   }

//   private buildWidget() {
//     const container = document.createElement('div');
//     container.className = 'jp-SplitButton-container';

//     const mainButton = new ToolbarButton({
//       className: 'jp-SplitButton-main',
//       label: 'Save to URL',
//       onClick: this.saveAction,
//       tooltip: 'Save notebook content to URL and copy to clipboard'
//     });

//     const settingsButton = new ToolbarButton({
//       className: 'jp-SplitButton-secondary',
//       icon: settingsIcon,
//       onClick: this.settingsAction,
//       tooltip: 'Save to URL Settings'
//     });

//     container.appendChild(mainButton.node);
//     container.appendChild(settingsButton.node);
//     this.node.appendChild(container);
//   }
// }

// In your main extension file:
// function addSaveToUrlButton(
//   app: JupyterFrontEnd,
//   notebookTracker: INotebookTracker
// ) {
//   let settings = {
//     copyOutput: false,
//     urlPath: '/jupyterlite/lab/index.html',
//     openAsNotebook: false
//   };

//   const saveAction = () => {
//     const current = notebookTracker.currentWidget;
//     console.log('in press', current, settings);
//     if (current) {
//       compressNotebookContent(current, settings);
//     }
//   };

//   const settingsAction = () => {
//     const dialog = new SettingsDialog(newSettings => {
//       settings = newSettings;
//       dialog.dispose();
//     }, settings);

//     showDialog({
//       title: 'Save to URL Settings',
//       body: dialog,
//       buttons: [Dialog.cancelButton()]
//     });
//   };

//   const splitButton = new SplitButton(saveAction, settingsAction);

//   notebookTracker.widgetAdded.connect((sender, panel) => {
//     console.log('added', splitButton, panel.toolbar);
//     panel.toolbar.insertItem(10, 'saveToUrl', splitButton);
//   });
// }

// Add "Save to URL" dropdown button to the notebook toolbar
function addSaveToUrlButton(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker
) {

  

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
        //dialog.dispose();
      }, settings);

      showDialog({
        title: 'Save to URL Settings',
        body: dialog,
        buttons: [Dialog.cancelButton(), Dialog.okButton()]
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
  id: 'urlify',
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
