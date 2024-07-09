import { JupyterFrontEnd, JupyterFrontEndPlugin, IRouter } from '@jupyterlab/application';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { INotebookTracker } from '@jupyterlab/notebook';
import { addSaveToUrlButton } from './toolbar';
import { addTempNotebookRoute } from './notebookRoute';
import { saveUrlParameters } from './urlUtils';

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