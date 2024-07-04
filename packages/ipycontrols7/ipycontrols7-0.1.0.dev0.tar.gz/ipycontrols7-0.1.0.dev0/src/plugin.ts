// Copyright (c) martinRenou
// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@lumino/application';

import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { JUPYTER_CONTROLS_VERSION } from 'jupyter-controls7/lib/version';
import * as widgetsExport from 'jupyter-controls7';
import 'jupyter-controls7/css/widgets.css';

const EXTENSION_ID = 'ipycontrols7:plugin';

/**
 * The example plugin.
 */
const controlsPlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true,
} as unknown as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default controlsPlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry
): void {
  console.log('registering controls for ipywidgets 7');
  console.log(JUPYTER_CONTROLS_VERSION, widgetsExport);
  registry.registerWidget({
    name: '@jupyter-widgets/controls',
    version: JUPYTER_CONTROLS_VERSION,
    exports: widgetsExport as unknown as any
  });
}
