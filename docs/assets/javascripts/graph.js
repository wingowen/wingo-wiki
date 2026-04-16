// Interactive Graph for Material for MkDocs
// Based on Apache ECharts

$(document).ready(function() {
  // Create graph container
  if ($('#graph-container').length === 0) {
    $('body').append('<div id="graph-container" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 9999; display: none;"><div id="graph" style="width: 100%; height: 100%;"></div><button id="close-graph" style="position: absolute; top: 20px; right: 20px; background: #333; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">Close</button></div>');
  }

  // Create graph button
  if ($('#open-graph').length === 0) {
    $('.md-header__buttons').append('<button id="open-graph" class="md-header__button" title="Open Graph"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg></button>');
  }

  // Open graph
  $('#open-graph').click(function() {
    $('#graph-container').show();
    initGraph();
  });

  // Close graph
  $('#close-graph').click(function() {
    $('#graph-container').hide();
  });

  // Initialize graph
  function initGraph() {
    var myChart = echarts.init(document.getElementById('graph'));

    // Sample data - this will be replaced by actual data from the plugin
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
      legend: {
        top: 'bottom',
        textStyle: {
          color: '#fff'
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

    // Handle window resize
    window.addEventListener('resize', function() {
      myChart.resize();
    });
  }
});

// Add CSS for graph button
var style = document.createElement('style');
style.innerHTML = `
  #open-graph {
    margin-right: 10px;
  }
  #open-graph:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;
document.head.appendChild(style);