import { JupyterFrontEnd, IRouter } from '@jupyterlab/application';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { NotebookModel } from '@jupyterlab/notebook';
import { UUID } from '@lumino/coreutils';
import { decompressSavedContent } from './urlUtils';

export function addTempNotebookRoute(
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

function updateUrlWithNotebookPath(notebookPath: string) {
  const url = new URL(window.location.href);
  
  // Get the current URL
  const currentUrl = window.location.href;

  // Extract the base URL up to /lab/index.html
  const baseUrlMatch = currentUrl.match(/(.*\/)lab\/index\.html/);
  const baseUrl = baseUrlMatch ? baseUrlMatch[1] : '';

  // JupyterLite
  let retroView = baseUrl + `notebooks/index.html?path=${notebookPath}&${notebookPath}&${url.search}&${url.hash}`;
  window.location.href = retroView;
}