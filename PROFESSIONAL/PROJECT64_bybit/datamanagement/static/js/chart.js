class ChartManager {
    constructor() {
      this.chart = null;
      this.xspan = null;
      this.klines = null;
      this.startPoint = null;
      this.lineSeries = null;
      this.isUpdatingLine = false;
      this.isHovered = false;
      this.isDragging = false;
      this.dragStartPoint = null;
      this.dragStartLineData = null;
      this.lastCrosshairPosition = null;
      this.candleseries = null;
      this.selectedPoint = null; //null/0/1
      this.hoverThreshold = 0.01;
      this.domElement = document.getElementById("tvchart");
      this.initializeChart();
      this.loadData();
    }
  

    updateTable() {
        console.log(3000)
        $.ajax({
            url: '/rest_update/',  // Replace with the actual URL of your Django view
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                updateChart(data.candles_data)
            },
            error: function () {
                console.error('Error fetching data from the server.');
            }
        });
    }

    updateChart(candles){

    }

    initializeChart() {
      const chartProperties = {
    width: 1200,
    height: 800,
    layout: {
      background: {
        color: '#000000'
      },
      textColor: '#ffffff'
    }
  };
      this.chart = LightweightCharts.createChart(
        this.domElement,
        chartProperties
      );
      this.candleseries = this.chart.addCandlestickSeries();
      this.lineSeries = this.chart.addLineSeries();
    }
  
    async loadData() {
      try {
        // const response = await fetch("./data.json");
        const response=
        const data = await response.json();
        this.klines = data.data.map((item) => ({
          time: Math.floor(new Date(item.time).getTime()),
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
        }));
  
        this.candleseries.setData(this.klines);
  
  
        for(let i=0;i<data.zones;i++){
          const key=(i).toString()
          const support_line=this.chart.addLineSeries({color: 'red', lineWidth:2,title: data.data[0][key].type+key});
          console.log(data.data[0][key])
          const support_data = data.data
          .filter((d) => d[key] && d[key].low !== '')
          .map((d) => ({ time: d.time, value: d[key].low }));
          // console.log(support_data)
          support_line.setData(support_data)
          // price=data.data
          // while()
  
          const resistance_line=this.chart.addLineSeries({color: 'green', lineWidth:2,title: data.data[0][key].type+key});
          const resistance_data = data.data
          .filter((d) => d[key] && d[key].high !== '')
          .map((d) => ({ time: d.time, value: d[key].high }));
          // console.log(support_data)
          resistance_line.setData(resistance_data)
        }
  
  
      } catch (error) {
        console.error("Error fetching or parsing data:", error);
      }
    }
  }
  
const chart=new ChartManager()
setInterval(chart.updateTable,1000);
  