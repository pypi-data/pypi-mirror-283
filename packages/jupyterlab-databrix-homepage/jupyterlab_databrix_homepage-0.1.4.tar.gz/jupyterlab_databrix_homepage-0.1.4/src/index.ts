import {
  ILabShell,
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {IDefaultFileBrowser } from '@jupyterlab/filebrowser';

import {
  ICommandPalette,
  MainAreaWidget,

} from '@jupyterlab/apputils';

import { DockPanel, TabBar, Widget } from '@lumino/widgets';
import { toArray } from '@lumino/algorithm';  

class databrixWidget extends Widget {
/**
* Construct a new databrix widget.
*/
constructor() {
  super();

  this.addClass('my-apodWidget');

  this.node.innerHTML = `

    <div class="container">
        <h1>Databrix Lab</h1>
        <p class="subtitle">Lernen Sie Data Science und Machine Learning in der Praxis!</p>
    </div>

    <div class="button-container">        
        <button data-commandLinker-command="nbgrader:open-assignment-list" class="button">
            <div class="icon"></div>
            <span>Praxisprojekte starten</span>
        </button>
      
        <button class="button secondary">
            <div class="icon"></div>
            <span>Gruppe wechseln</span>
        </button>
    </div>

    <div class="contact">
            <h2>Kontakt</h2>
            <p>Bei Fragen kontaktieren Sie bitte uns an admin@databrix.org!</p>
    </div>

      `;
}
}

/**
 * Initialization data for the jupyterlab_apod extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'databrix-homepage',
  description: 'A JupyterLab extension for homepage databrix lab.',
  autoStart: true,
  requires: [ICommandPalette,ILabShell],
  optional: [ILayoutRestorer],   
  activate: activate
};



function activate(app: JupyterFrontEnd,
                palette: ICommandPalette, 
                labShell: ILabShell,
                restorer: ILayoutRestorer | null,
                defaultBrowser: IDefaultFileBrowser | null) {
console.log('JupyterLab extension databrix homepage is activated!');
// Declare a widget variable
let widget: MainAreaWidget<databrixWidget>;

// Add an application command
const command: string = 'launcher:create';
app.commands.addCommand(command, {
  label: 'Databrix Lab Homepage',
  
  execute: () => {
   
    const content = new databrixWidget();
    widget = new MainAreaWidget({content});
    const id = `home-${Private.id++}`;
    widget.id = id
    widget.title.label = 'Databrix Lab Home';
    widget.title.closable = true;
    
    app.shell.add(widget, 'main');
  
    app.shell.activateById(widget.id);


    labShell.layoutModified.connect(() => {
      // If there is only a launcher open, remove the close icon.
      widget.title.closable = toArray(app.shell.widgets('main')).length > 1;
    }, widget);
  }
});

if (labShell) {
  void Promise.all([app.restored, defaultBrowser?.model.restored]).then(
    () => {
      function maybeCreate() {
        // Create a launcher if there are no open items.
        if (labShell!.isEmpty('main')) {
          void app.commands.execute(command);
        }
      }
      // When layout is modified, create a launcher if there are no open items.
      labShell.layoutModified.connect(() => {
        maybeCreate();
      });
    }
  );
}  

palette.addItem({
  command: command,
  category: ('Databrix')
});

if (labShell) {
  labShell.addButtonEnabled = true;
  labShell.addRequested.connect((sender: DockPanel, arg: TabBar<Widget>) => {
    // Get the ref for the current tab of the tabbar which the add button was clicked
    const ref =
      arg.currentTitle?.owner.id ||
      arg.titles[arg.titles.length - 1].owner.id;

    return app.commands.execute(command, { ref });
  });
}


}



export default plugin;


/**
* The namespace for module private data.
*/
namespace Private {
/**
 * The incrementing id used for launcher widgets.
 */
export let id = 0;
}
