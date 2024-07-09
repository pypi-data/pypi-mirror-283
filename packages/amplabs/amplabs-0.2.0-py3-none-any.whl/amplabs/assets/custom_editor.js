document.addEventListener("DOMContentLoaded", function () {
  function initializeAceEditor(yamlContent) {
    var editorDiv = document.getElementById("editor");
    if (editorDiv && typeof ace !== "undefined") {
      var editor = ace.edit("editor");
      editor.renderer.setScrollMargin(10, 10, 10, 10);
      editor.setFontSize(14);
      editor.setTheme("ace/theme/xcode");
      editor.session.setMode("ace/mode/yaml");
      // if (!editorInitialized) {
      editor.session.setValue(yamlContent);
      // }
    } else {
      setTimeout(function () {
        initializeAceEditor(yamlContent);
      }, 50);
    }
  }

  function convertJsonToYaml(jsonContent) {
    try {
      var jsonData = JSON.parse(jsonContent);
      var yamlContent = jsyaml.dump(jsonData);
      return yamlContent;
    } catch (e) {
      console.error("Invalid JSON:", e);
      return "";
    }
  }

  function getEditorContent() {
    var editor = ace.edit("editor");
    var yamlString = editor.session.getValue();
    const yamlObject = jsyaml.load(yamlString);
    const jsonString = JSON.stringify(yamlObject, null, 2);
    return jsonString;
  }

  window.initializeAceEditor = initializeAceEditor;
  window.convertJsonToYaml = convertJsonToYaml;
  window.getEditorContent = getEditorContent;
});
