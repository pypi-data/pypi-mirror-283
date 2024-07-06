import * as LZString from 'lz-string';
import {
  NotebookModel,

} from '@jupyterlab/notebook';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Dialog, showDialog } from '@jupyterlab/apputils';

import { UUID } from '@lumino/coreutils';


import { INotebookTracker } from '@jupyterlab/notebook';
import { ToolbarButton } from '@jupyterlab/apputils';

import { Clipboard } from '@jupyterlab/apputils';

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

  // If available, Add to the router
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
            await app.commands.execute('notebook:open-temp', {
            });
          }
        };

        router.routed.connect(createFromURLRoute);
      }
    });

    app.commands.addCommand('notebook:open-temp', {
      label: 'Open Temporary Notebook',
      execute: async args => {
        // Utility function to create a new notebook.
        const createNew = async (
          cwd: string,
          kernelId: string,
          kernelName: string
        ) => {

          const model = await app.commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'notebook'
          });

          console.log('created model', model);

          if (model !== undefined) {
            const widget = (await app.commands.execute('docmanager:open', {
              path: model.path,
              factory: 'Notebook',
              kernel: { id: kernelId, name: kernelName }
            })) 

            widget.isUntitled = true;

            const tempId = `temp-notebook-${UUID.uuid4()}`;
            
            await widget.context.rename(tempId + '.ipynb');


            // set content of widget 
            const content = decompressSavedContent();
            if (content) {
              // Load the content into the notebook model
              const notebookModel = widget.context.model as NotebookModel;
              console.log('model', notebookModel);
              notebookModel.fromJSON(content);
    
              // Save the notebook context to ensure the content is written to disk
              await widget.context.save();
              console.log('Notebook content saved.');
            }
            


            // After creating the notebook, update the URL with the notebook path
            updateUrlWithNotebookPath(widget.context.path);


            return widget;
          }
        };

        const currentBrowser =
          filebrowserFactory?.tracker.currentWidget ??
          //@ts-ignore
          filebrowserFactory.defaultBrowser;
        const cwd =
          (args['cwd'] as string) || (currentBrowser?.model.path ?? '');
        const kernelId = (args['kernelId'] as string) || '';
        const kernelName = (args['kernelName'] as string) || '';

        const model = await createNew(cwd, kernelId, kernelName);
        console.log(
          'created model',
          model,
          cwd,
          'kernel',
          kernelId,
          'kernelName',
          kernelName
        );
      }
    });

    // Function to update the URL with the notebook path
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
  }
}


// Compress the notebook text, set as URL parameter, and copy to clipboard
async function compressNotebookContent(notebookPanel: any, settings: ISettingRegistry.ISettings) {
  const copyOutput = settings.get('copyOutput').composite as boolean;
  const urlPath = settings.get('urlPath').composite as string;

  let notebookContent: any;
  if (copyOutput) {
    notebookContent = notebookPanel.context.model.toJSON();
  } else {
    notebookContent = notebookPanel.context.model.toJSON();
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
  url.pathname = urlPath;

  // Add the hash and query parameters
  url.hash = `notebook=${compressedContent}`;
  url.searchParams.set('tempNotebook', '1');
  url.searchParams.set('path', 'temp.ipynb');
  console.log('new url', url, url.toString());

  const newUrl = url.toString();
  Clipboard.copyToSystem(newUrl);
}

// Add "Save to URL" button to the notebook toolbar
function addSaveToUrlButton(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker,
  settings: ISettingRegistry.ISettings
) {
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

  notebookTracker.widgetAdded.connect((sender, panel) => {
    panel.toolbar.insertItem(10, 'saveToUrl', saveToUrlButton);
  });
}

import {
  IFileBrowserFactory,
} from '@jupyterlab/filebrowser';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'urlify-nb',
  autoStart: true,
  requires: [IFileBrowserFactory, IRouter, INotebookTracker, ISettingRegistry],
  activate: async (
    app: JupyterFrontEnd,
    filebrowserFactory: IFileBrowserFactory,
    router: IRouter,
    notebookTracker: INotebookTracker,
    settingRegistry: ISettingRegistry
  ) => {
    try {
      console.log('Activating ephemeral-notebooks extension');

      // Load the settings
      const settings = await settingRegistry.load(extension.id);

      router.register({
        command: 'notebook:start-nav',
        pattern: /(tempNotebook=1)/,
        rank: 20
      });

      addSaveToUrlButton(app, notebookTracker, settings);
      saveUrlParameters();
      await addTempNotebookRoute(app, filebrowserFactory, router);

      console.log('ephemeral-notebooks extension activated successfully');
    } catch (error) {
      console.error('Error activating ephemeral-notebooks extension:', error);
    }
  }
};

export default extension;
