window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    handle_sidebar: function (n_clicks, json_content, is_open) {
      if (n_clicks > 0) {
        var yamlContent = window.convertJsonToYaml(json_content);
        setTimeout(function () {
          window.initializeAceEditor(yamlContent);
        }, 50);
        return !is_open;
      }
      return is_open;
    },
    handle_save_config: function (n_clicks, data) {
      if (n_clicks > 0) {
        try {
          var yamlContent = window.getEditorContent();
          if (yamlContent === undefined) return yamlContent;
          var content = JSON.parse(yamlContent);
          if (parseFloat(content?.["plot_area"]?.["width"]) < 350) {
            alert("Plot Width should be greater than 350");
            return window.dash_clientside.no_update;
          }
          if (parseFloat(content?.["plot_area"]?.["height"]) < 350) {
            alert("Plot Height should be greater than 350");
            return window.dash_clientside.no_update;
          }
          return yamlContent;
        } catch (error) {
          console.log(error);
        }
      }
      return data;
    },
    adjust_plot_size: function (updated_size, json_config) {
      json_data = JSON.parse(json_config);
      console.log("INSIDE CALLLBACK");
      if (json_data?.["plot_area"]?.["width"] == undefined) {
        return window.dash_clientside.no_update;
      }
      if (updated_size == false) {
        var wrapperDiv = document
          .getElementById("graph")
          .getElementsByClassName("js-plotly-plot")[0];
        var graphDiv = document
          .getElementById("graph")
          .querySelector(".svg-container");
        if (!graphDiv || !graphDiv) return;

        var visualRect = graphDiv.querySelector(".nsewdrag ");

        var entireFigureHeight = graphDiv.getBoundingClientRect().height;
        var entireFigureWidth = graphDiv.getBoundingClientRect().width;

        var initialPlotHeight = visualRect.getBoundingClientRect().height;
        var initialPlotWidth = visualRect.getBoundingClientRect().width;
        console.log(
          2 * entireFigureHeight - initialPlotHeight,
          2 * entireFigureWidth - initialPlotWidth
        );
        var new_height = 2 * entireFigureHeight - initialPlotHeight;
        var new_width = 2 * entireFigureWidth - initialPlotWidth;
        if (new_height > 0 && new_width > 0) {
          Plotly.relayout(wrapperDiv, {
            height: new_height,
            width: new_width,
          });
        }
      }
    },
  },
});
