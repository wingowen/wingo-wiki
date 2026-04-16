// Interactive Graph for Material for MkDocs
// Based on Apache ECharts

// Create floating button immediately when script loads
(function() {
  // Create graph container
  var container = document.createElement('div');
  container.id = 'graph-container';
  container.innerHTML = '<div id="graph" style="width: 100%; height: 100%;"></div><button id="close-graph" style="position: absolute; top: 20px; right: 20px; background: #333; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; z-index: 10000;">Close</button>';
  container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 9999; display: none;';
  document.body.appendChild(container);

  // Create floating graph button
  var button = document.createElement('button');
  button.id = 'floating-graph-btn';
  button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
  button.title = 'Open Knowledge Graph';
  button.style.cssText = 'position: fixed; bottom: 30px; right: 30px; width: 56px; height: 56px; border-radius: 50%; background: #4f46e5; color: white; border: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); cursor: pointer; z-index: 9998; display: flex; align-items: center; justify-content: center; transition: transform 0.2s, box-shadow 0.2s;';
  
  // Button hover effect
  button.onmouseover = function() {
    this.style.transform = 'scale(1.1)';
    this.style.boxShadow = '0 6px 16px rgba(79, 70, 229, 0.5)';
  };
  button.onmouseout = function() {
    this.style.transform = 'scale(1)';
    this.style.boxShadow = '0 4px 12px rgba(79, 70, 229, 0.4)';
  };
  
  document.body.appendChild(button);

  // Open graph
  button.onclick = function() {
    document.getElementById('graph-container').style.display = 'block';
    initGraph();
  };

  // Close graph
  document.getElementById('close-graph').onclick = function() {
    document.getElementById('graph-container').style.display = 'none';
  };

  // Initialize graph function
  function initGraph() {
    if (typeof echarts !== 'undefined') {
      var myChart = echarts.init(document.getElementById('graph'));

      var option = {
        title: {
          text: 'Wingo Wiki Knowledge Graph',
          left: 'center',
          top: 20,
          textStyle: {
            color: '#fff',
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return params.data.name;
          },
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderColor: '#4f46e5',
          borderWidth: 1
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            data: [
              {name: 'AI Agent', symbolSize: 50, category: 0},
              {name: 'LangGraph', symbolSize: 40, category: 1},
              {name: 'ReAct', symbolSize: 30, category: 1},
              {name: 'RAG', symbolSize: 35, category: 2},
              {name: 'HyDE', symbolSize: 25, category: 2},
              {name: 'MCP', symbolSize: 45, category: 3}
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
              color: '#fff',
              fontSize: 12
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3,
              width: 2
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 4
              }
            },
            force: {
              repulsion: 800,
              edgeLength: 100,
              gravity: 0.1
            }
          }
        ]
      };

      myChart.setOption(option);

      window.addEventListener('resize', function() {
        myChart.resize();
      });
    } else {
      console.log('ECharts not loaded yet, retrying...');
      setTimeout(initGraph, 500);
    }
  }
})();