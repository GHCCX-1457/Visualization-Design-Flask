new Vue({
    el:'#app',
    data(){
        return{
            name:['line','bar','rose','funnel','boxplot']
        }
    },
    mounted() {
      for (let i = 0; i < 6; i++) {
        axios({
          methods: "get",
          url: '../' + this.name[i] + 'Chart2',
        }).then(resp => {
          echarts.init(document.getElementById(this.name[i]),
              'white', {renderer: 'canvas'}).setOption(resp.data);
        })
      }
    }
    })

