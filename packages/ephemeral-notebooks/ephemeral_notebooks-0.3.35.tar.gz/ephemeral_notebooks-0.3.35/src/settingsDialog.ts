import { Widget } from '@lumino/widgets';

export class SettingsDialog extends Widget {
  private settings: {
    copyOutput: boolean;
    urlPath: string;
    openAsNotebook: boolean;
  };
  private container: HTMLDivElement;

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
    this.container = document.createElement('div');
    this.node.appendChild(this.container);
    this.buildDialog();
  }

  private buildDialog() {
    this.container.innerHTML = '';
    this.container.style.padding = '20px';
    this.container.style.maxWidth = '400px';
    this.container.style.width = '100%';
    this.container.style.boxSizing = 'border-box';
    this.container.style.fontFamily = 'Arial, sans-serif';

    const copyOutputSwitch = this.createSwitchControl(
      'Copy notebook output',
      this.settings.copyOutput,
      (checked) => this.updateSettings({ copyOutput: checked })
    );
    this.container.appendChild(copyOutputSwitch);

    const urlPathLabel = document.createElement('label');
    urlPathLabel.style.display = 'block';
    urlPathLabel.style.marginTop = '20px';
    urlPathLabel.style.marginBottom = '8px';
    urlPathLabel.style.fontWeight = 'bold';
    urlPathLabel.textContent = 'URL path:';
    this.container.appendChild(urlPathLabel);

    const urlPathSelect = document.createElement('select');
    urlPathSelect.style.width = '100%';
    urlPathSelect.style.padding = '8px';
    urlPathSelect.style.marginBottom = '15px';
    urlPathSelect.style.borderRadius = '4px';
    urlPathSelect.style.border = '1px solid #ccc';

    const paths = [
      { label: 'JupyterLite', value: '/jupyterlite/lab/index.html', openAsNotebook: false },
      { label: 'JupyterLite Notebook', value: '/jupyterlite/lab/index.html', openAsNotebook: true },
      { label: 'JupyterLab', value: '/lab/index.html', openAsNotebook: false },
      { label: 'Custom', value: 'custom', openAsNotebook: false }
    ];

    paths.forEach(path => {
      const option = document.createElement('option');
      option.value = JSON.stringify(path);
      option.textContent = path.label;
      if (path.value === this.settings.urlPath && path.openAsNotebook === this.settings.openAsNotebook) {
        option.selected = true;
      }
      urlPathSelect.appendChild(option);
    });

    this.container.appendChild(urlPathSelect);

    const urlDisplay = document.createElement('p');
    urlDisplay.style.fontSize = '0.9em';
    urlDisplay.style.color = '#666';
    urlDisplay.style.marginTop = '10px';
    urlDisplay.style.marginBottom = '15px';
    urlDisplay.style.wordBreak = 'break-all';
    this.container.appendChild(urlDisplay);

    const customUrlInput = document.createElement('input');
    customUrlInput.type = 'text';
    customUrlInput.placeholder = 'Enter custom URL path';
    customUrlInput.style.width = '100%';
    customUrlInput.style.padding = '8px';
    customUrlInput.style.marginTop = '10px';
    customUrlInput.style.display = 'none';
    customUrlInput.style.boxSizing = 'border-box';
    customUrlInput.style.borderRadius = '4px';
    customUrlInput.style.border = '1px solid #ccc';
    this.container.appendChild(customUrlInput);

    const warningMessage = document.createElement('p');
    warningMessage.textContent = 'Warning: urlify must be installed on the Jupyter instance for custom URLs.';
    warningMessage.style.color = 'orange';
    warningMessage.style.fontSize = '0.9em';
    warningMessage.style.display = 'none';
    warningMessage.style.marginTop = '10px';
    this.container.appendChild(warningMessage);

    urlPathSelect.addEventListener('change', () => {
      const selectedOption = JSON.parse(urlPathSelect.value);
      if (selectedOption.value === 'custom') {
        customUrlInput.style.display = 'block';
        warningMessage.style.display = 'block';
        urlDisplay.textContent = '';
        customUrlInput.value = '';
      } else {
        customUrlInput.style.display = 'none';
        warningMessage.style.display = 'none';
        this.updateSettings({ 
          urlPath: selectedOption.value, 
          openAsNotebook: selectedOption.openAsNotebook 
        });
        this.updateUrlDisplay(urlDisplay, selectedOption.value, false);
      }
    });

    customUrlInput.addEventListener('input', () => {
      this.updateSettings({ 
        urlPath: customUrlInput.value, 
        openAsNotebook: false 
      });
      this.updateUrlDisplay(urlDisplay, customUrlInput.value, true);
    });

    this.updateUrlDisplay(urlDisplay, this.settings.urlPath, this.settings.urlPath === 'custom');
  }

  private createSwitchControl(label: string, initialState: boolean, onChange: (checked: boolean) => void) {
    const container = document.createElement('label');
    container.style.display = 'flex';
    container.style.alignItems = 'center';
    container.style.marginBottom = '15px';
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

  private updateSettings(partialSettings: Partial<{ copyOutput: boolean; urlPath: string; openAsNotebook: boolean }>) {
    this.settings = { ...this.settings, ...partialSettings };
    this.onSettingsChange(this.settings);
  }

  private updateUrlDisplay(element: HTMLElement, urlPath: string, isCustom: boolean) {
    if (isCustom) {
      element.textContent = `Links to: ${urlPath}`;
    } else {
      const baseUrl = window.location.href.split('/lab')[0];
      element.textContent = `Links to: ${baseUrl}${urlPath}`;
    }
  }
}