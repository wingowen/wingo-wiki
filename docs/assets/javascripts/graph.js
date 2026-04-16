// Interactive Graph for Material for MkDocs
// Based on Apache ECharts

document.addEventListener('DOMContentLoaded', function() {
  // Wait for jQuery and ECharts to load
  function initGraphButton() {
    // Create graph container
    if (!document.getElementById('graph-container')) {
      var container = document.createElement('div');
      container.id = 'graph-container';
      container.innerHTML = '<div id="graph" style="width: 100%; height: 100%;"></div><button id="close-graph" style="position: absolute; top: 20px; right: 20px; background: #333; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">Close</button>';
      container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 9999; display: none;';
      document.body.appendChild(container);
    }

    // Create graph button
    if (!document.getElementById('open-graph')) {
      var headerButtons = document.querySelector('.md-header__buttons');
      if (headerButtons) {
        var button = document.createElement('button');
        button.id = 'open-graph';
        button.className = 'md-header__button';
        button.title = 'Open Graph';
        button.setAttribute('aria-label', 'Open Graph');
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
        button.style.cssText = 'margin-right: 10px;';
        headerButtons.insertBefore(button, headerButtons.firstChild);
        
        // Open graph
        button.addEventListener('click', function() {
          document.getElementById('graph-container').style.display = 'block';
          initGraph();
        });
      }
    }

    // Close graph
    var closeBtn = document.getElementById('close-graph');
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        document.getElementById('graph-container').style.display = 'none';
      });
    }
  }

  // Initialize graph
  function initGraph() {
    if (typeof echarts !== 'undefined') {
      var myChart = echarts.init(document.getElementById('graph'));

      var option = {
        title: {
          text: 'Knowledge Graph',
          left: 'center',
          textStyle: {
            color: '#fff'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return params.data.name;
          }
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            data: [
              {name: 'AI Agent', symbolSize: 50},
              {name: 'LangGraph', symbolSize: 40},
              {name: 'ReAct', symbolSize: 30},
              {name: 'RAG', symbolSize: 35},
              {name: 'HyDE', symbolSize: 25},
              {name: 'MCP', symbolSize: 45}
            ],
            links: [
              {source: 'AI Agent', target: 'LangGraph'},
              {source: 'AI Agent', target: 'ReAct'},
              {source: 'AI Agent', target: 'RAG'},
              {source: 'RAG', target: 'HyDE'},
              {source: 'AI Agent', target: 'MCP'}
            ],
            roam: true,
            label: {
              show: true,
              color: '#fff'
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            },
            emphasis: {
              lineStyle: {
                width: 4
              }
            },
            force: {
              repulsion: 1000,
              edgeLength: [80, 120]
            }
          }
        ]
      };

      myChart.setOption(option);

      window.addEventListener('resize', function() {
        myChart.resize();
      });
    }
  }

  // Try to initialize immediately
  initGraphButton();

  // Also try again after a short delay in case header is not yet rendered
  setTimeout(initGraphButton, 1000);
  setTimeout(initGraphButton, 3000);
});