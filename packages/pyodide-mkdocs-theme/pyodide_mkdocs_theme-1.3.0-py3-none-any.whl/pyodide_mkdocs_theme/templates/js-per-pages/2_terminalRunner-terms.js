/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/




class _TerminalHandler extends PyodideSectionsRunner {

  constructor(id){
    super(id)
    this.terminal = null
    this.topDiv = null
    this.termEnabled = false
    this.isIsolated = id.startsWith("term_only")
    // this.alreadyRanPost = false
  }

  handleTerminalWidthTroubles(){
    const wWrapper = this.topDiv.width()
    if(wWrapper != this.terminal.width()){
      this.terminal.width(wWrapper)
    }
  }

  addEventToRunOnce(target, event, cbk, withLock=false){
    let clickHandler = async _=>{
      target.off(event, clickHandler)
      cbk()
    }
    if(withLock){
      clickHandler = withPyodideAsyncLock('term_'+event, clickHandler)
    }
    target.on('click', clickHandler)
  }


  /**Build a jQuery terminal and bind it to the underlying pyodide runtime.
   *
   * WARNING:  If this is an IdeEditorHandler, this.id is the id of the editor div, not
   *           the id of the terminal div ! (hence the use of the termId argument)
   * */
  build(termId=null){
    if(!termId) termId = this.id
    const jqTermId = '#' + termId

    jsLogger("[Terminal] - build " + jqTermId)

    const commandsCbk = this.getAsyncPythonExecutor()
    const termOptions = {
      greetings: "",                    // cancel terminal banner (welcome message),
      completionEscape: false,
      prompt: CONFIG.MSG.promptStart,
      outputLimit: this.stdoutCutOff,
      enabled: false,                   // GET RID OF THE DAMN AUTO-SCROLL!!!!!!
      // wrap: getWrapTerms(),          // Also deactivate colors... FUCK THIS!
      keymap: this.getTerminalBindings(),
      completion: function (command, callback) {
        callback(pyFuncs.pyconsole.complete(command).toJs()[0]);    // autocompletion
      },
      onBlur: function(){}, // Allow to leave the textarea, focus-wise.
                            // DO NOT PUT ANY CODE INSIDE THIS !!
    }

    this.terminal = $(jqTermId).terminal(commandsCbk, termOptions)
    this.topDiv   = this.terminal.closest(".py_mk_wrapper")

    if(CONFIG._devMode) CONFIG.terms[termId]=this.terminal

    // Since terminal are created deactivated, add an EventListener for click to reactivate
    // them (once only: unsubscribe the listener on click. Note: no original click event)
    // Using the async lock so that the user cannot resume a terminal while it's running
    // (could occur on first click/run).
    this.addEventToRunOnce(this.terminal, 'click',  _=>{
      if(this.termEnabled) return;
      this.terminal.focus(true).enable()
      this.termEnabled = true
    }, true)
    this.prefillTermIfAny()

    /* Try to fix:
        - The "terminal with 0px with in tabbed IDEs/terminals":
        - The FILL content lost when the user changed of tab somewhere in the page...
    */
    const wrapper = this.terminal.parent()
    wrapper.on('click', _=>{
      const w = wrapper.css('width'), h = wrapper.css('height')
      if(w != this.terminal.css('width') || h != this.terminal.css('height')){
        this.terminal.css('width', w)
        this.terminal.css('height', h)
      }

      if(this.isIsolated && !this.terminal.get_command()){
        this.prefillTermIfAny()
      }
    })

    super.build()   // nothing done so far, but for consistency...
  }




  /**Hook returning the configuration for terminal keyboard shortcuts bindings.
   * To override in child classes when needed.
   *
   * Handled here: transfer KeyInterrupt from DOM to python runtime (note: actually
   * useless as long as no worker used!).
   * */
  getTerminalBindings(){
    return ({
      "CTRL+C": async (e) => {
        const txt = getSelectionText()

        // Skip if some text is selected (=copy!)
        if (!txt) {
          let currentCmd = this.terminal.get_command();
          pyFuncs.clear_console();    // Looks like it does nothing...? :/
          this.terminal.echo(CONFIG.MSG.promptStart + currentCmd);
          this.terminal.echo(error("KeyboardInterrupt"));
          this.terminal.set_command("");
          this.terminal.set_prompt(CONFIG.MSG.promptStart);

        }else if(CONFIG.joinTerminalLines){
          // If not activated, rely on the original clipboard event, so that the user still can
          // copy content if the browser complains with this functionality.
          e.preventDefault()
          e.stopPropagation()
          await navigator.clipboard.writeText(txt.replace(/\n/g, ''))
        }
      }
    })
  }

  getAsyncPythonExecutor(){
    throw new Error('Should be overridden in the child class.')
  }


  prefillTermIfAny(){
    if(this.prefillTerm) this.terminal.set_command(this.prefillTerm)
  }

}









class TerminalRunner extends _TerminalHandler {


  /**When a terminal is available, display stdout and errors in it, if any.
   * */
  giveFeedback(stdout, stdErr="", _){
    if(stdErr){
      stdErr = error(stdErr)
    }else if(stdout.endsWith('\n')){
      stdout = stdout.slice(0,-1)       // useful when printing from terminal and no error
    }
    const msg = stdout + stdErr
    if(msg) this.terminal.echo(msg)
    return msg
  }


  globalTearDown(){
    this.terminal.resume()
    super.globalTearDown()
  }


  /**Generate the async-locked callback used to run commands typed into the terminal.
   *
   * WARNING: USE `super.[...]` !
   *
   * Using super calls, because one only wants the setup specific to terminal here, while "this"
   * could be an IdeRunner object. Ine that case, this.setupRuntime would run the setup for the
   * code in the editor, and not the command typed in the terminal.
   * This also way work with TerminalRunners, because the generic setupRuntime is _NOT_ on the
   * TerminalRunner class, but actually on the PythonSectionRunner one.
   *
   * For the very same kind of reasons, the `options` used cannot be the ones returned as usual
   * by this.runPythonCodeWithOptionsIfNoStdErr, because the terminal commands are run async, so store
   * locally the needed version.
   */
  getAsyncPythonExecutor(){

    const commandsBuffer = []
    return withPyodideAsyncLock('terminal', async (command) => {

      commandsBuffer.push(command)
      const currentCmd = commandsBuffer.join('\n')
      this.storeUserCodeInPython('__USER_CMD__', currentCmd)
      this.terminal.pause()

      let options
      try{
        /* Any ASYNC potential calls to setupRuntime HAVE to be done before the pyconsole.push,
           otherwise, because of async loop scheduling, the environment is setup AFTER the user
           command has been run...
           Because of this, need the commandBuffer to update the __USER_CMD__ variable, and
           _also_ because of this, the env section will also run on incomplete commands, and
           _also_ because of this, any import done through the console must be checked now...
        */

        // If an IDE-terminal is run before the IDE itself, it must run the env/post sections.
        // If env already run before, envTerm HAS to run independently, so remove the dependency.
        if(!this.alreadyRanEnv){
          options = await super.setupRuntime()
        }else{
          options = this.buildRunConfig()
          options.graphEnvRuns.envTerm = ''
        }
        await this.runEnvironmentAsync(options, 'envTerm')
        if(options.userRunnable){
            await this.runTermCommand(options, command, commandsBuffer, currentCmd)
        }

      } finally {
        await this.runEnvironmentAsync(options, 'postTerm')
        await this.runEnvironmentAsync(options, 'post')
        this.globalTearDown()
        this.storeUserCodeInPython('__USER_CMD__', "")
      }
    })
  }


  async runTermCommand(options, command, commandsBuffer, currentCmd){

    try{
      // Must be done BEFORE creating the future, otherwise, async scheduling troubles,
      await this.installAndImportMissingModules(currentCmd, options)

    }catch(err){
      /* BUT, if ever this fails, the commandBuffer has to be reset, otherwise the failing import
        will keep being repeated. */
      commandsBuffer.length=0
      ;[options.stdErr, _] = generateErrorLog(err)
      this.giveFeedback("", options.stdErr)
      return
    }

    // multiline commands should be split (useful when pasting)
    for (let c of command.split("\n")) {

      let future = pyFuncs.pyconsole.push(c);

      // set the beginning of the next line in the terminal:
      const isIncompleteExpr = future.syntax_check=="incomplete"
      const headLine = isIncompleteExpr ? CONFIG.MSG.promptWait : CONFIG.MSG.promptStart
      this.terminal.set_prompt(headLine);

      switch (future.syntax_check) {
        case "complete":

            try{
              /* NOTE: nothing can be awaited in between the future "creation" and the
                execution of options.runCodeAsync, otherwise the event loop will actually
                compute the result of the python command (which is already stored in the
                event loop, now) before the restrictions are put in place in the environment
                (everything is synch up to this...).
              */
              options.runCodeAsync = async _=>{ await pyFuncs.await_fut(future) }
              await this.runPythonCodeWithOptionsIfNoStdErr(command, options)

            }finally{
              commandsBuffer.length = 0
              future.destroy()    // to destroy only if it got awaited first
              await sleep()       // Enforce GUI update, going through the next tick
            }

        case "incomplete":
          continue          // complete also goes there...

        case "syntax-error":
          commandsBuffer.length = 0
          this.terminal.error(future.formatted_error.trimEnd());
          continue
        default:
          commandsBuffer.length = 0
          throw new Error(`Unexpected state ${future.syntax_check}`);
      }
    }
  }
}